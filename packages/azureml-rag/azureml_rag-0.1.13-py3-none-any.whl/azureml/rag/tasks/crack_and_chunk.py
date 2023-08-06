# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
import pandas as pd
from pathlib import Path
import time
from typing import Iterator, List
import re
import time
import traceback

from azureml.rag.utils.logging import get_logger, enable_stdout_logging, enable_appinsights_logging, track_activity, _logger_factory
from azureml.rag.documents import SUPPORTED_EXTENSIONS, DocumentChunksIterator, DocumentSource, Document, split_documents


logger = get_logger('crack_and_chunk')


def chunks_to_dataframe(chunks) -> pd.DataFrame:
    metadata = []
    data = []
    for chunk in chunks:
        metadata.append(json.dumps(chunk.get_metadata()))
        data.append(chunk.load_data())
    #(metadata, data) = [(json.dumps(chunk.metadata), chunk.load_data()) for chunk in chunks]
    chunks_dict = {
        "Metadata": metadata,
        "Chunk": data
    }

    return pd.DataFrame(chunks_dict)


def write_chunks_to_csv(chunks_df, output_path):
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    chunks_df.to_csv(output_path, index=False)


def write_chunks_to_jsonl(chunks: List[Document], output_path):
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        for chunk in chunks:
            f.write(chunk.dumps())
            f.write('\n')


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False


def main(args, logger, activity_logger):
    splitter_args = {'chunk_size': args.chunk_size, 'chunk_overlap': args.chunk_overlap, 'use_rcts': args.use_rcts}

    def filter_and_log_extensions(sources: Iterator[DocumentSource], allowed_extensions=SUPPORTED_EXTENSIONS) -> Iterator[DocumentSource]:
        """Filter out sources with extensions not in allowed_extensions."""
        total_files = 0
        skipped_files = 0
        skipped_extensions = {}
        kept_extension = {}
        for source in sources:
            total_files += 1
            if allowed_extensions is not None:
                if source.path.suffix not in allowed_extensions:
                    skipped_files += 1
                    ext_skipped = skipped_extensions.get(source.path.suffix, 0)
                    skipped_extensions[source.path.suffix] = ext_skipped + 1
                    logger.debug(f'Filtering out extension "{source.path.suffix}" source: {source.filename}')
                    continue
            ext_kept = kept_extension.get(source.path.suffix, 0)
            kept_extension[source.path.suffix] = ext_kept + 1
            logger.info(f'Processing file: {source.filename}')
            yield source
        logger.info(f"[DocumentChunksIterator::filter_extensions] Filtered {skipped_files} files out of {total_files}")
        logger.info(f"[DocumentChunksIterator::filter_extensions] Skipped extensions: {json.dumps(skipped_extensions, indent=2)}")
        logger.info(f"[DocumentChunksIterator::filter_extensions] Kept extensions: {json.dumps(kept_extension, indent=2)}")
        activity_logger.activity_info['total_files'] = total_files
        activity_logger.activity_info['skipped_files'] = skipped_files
        activity_logger.activity_info['skipped_extensions'] = json.dumps(skipped_extensions)
        activity_logger.activity_info['kept_extensions'] = json.dumps(kept_extension)

    chunked_documents = DocumentChunksIterator(
        files_source=args.input_data,
        glob=args.input_glob,
        base_url=args.data_source_url,
        document_path_replacement_regex=args.document_path_replacement_regex,
        file_filter=filter_and_log_extensions,
        chunked_document_processors = [lambda docs: split_documents(docs, splitter_args=splitter_args)],
    )
    file_count = 0
    total_time = 0
    for chunked_document in chunked_documents:
        file_start_time = time.time()
        file_count += 1
        # TODO: Ideally make it easy to limit number of files with a `- take: n` operation on input URI in MLTable
        if (args.max_sample_files != -1 and file_count >= args.max_sample_files):
            logger.info(f"file count: {file_count} - reached max sample file count: {args.max_sample_files}", extra={'print': True})
            break
        if args.output_format == "csv":
            write_chunks_to_csv(chunks_to_dataframe(chunked_document.chunks), Path(args.output_title_chunk) / f"Chunks_{Path(chunked_document.source.filename).name}.csv")
        elif args.output_format == "jsonl":
            write_chunks_to_jsonl(chunked_document.chunks, Path(args.output_title_chunk) / f"Chunks_{Path(chunked_document.source.filename).name}.jsonl")
        file_end_time = time.time()
        total_time += file_end_time - file_start_time

    logger.info(f"Processed {file_count} files",)
    activity_logger.activity_info["file_count"] = str(file_count)

    if file_count == 0:
        logger.info(f"No chunked documents found in {args.input_data} with glob {args.input_glob}")
        activity_logger.activity_info["error"] = "No chunks found"
        activity_logger.activity_info["glob"] = args.input_glob if re.match("^[*/\\\"']+$", args.input_glob) is not None else "[REDACTED]"
        raise ValueError(f"No chunked documents found in {args.input_data} with glob {args.input_glob}.")

    logger.info(f"Wrote chunks to {file_count} files in {total_time} seconds (chunk generation time excluded)")
    activity_logger.activity_info["file_count"] = file_count


def main_wrapper(args, logger):
    with track_activity(logger, "crack_and_chunk") as activity_logger:
        try:
            main(args, logger, activity_logger)
        except Exception:
            activity_logger.error(f"crack_and_chunk failed with exception: {traceback.format_exc()}")  # activity_logger doesn't log traceback
            raise

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_data", type=str)
    parser.add_argument("--input_glob", type=str, default="**/*")
    parser.add_argument("--allowed_extensions", required=False, type=str, default=",".join(SUPPORTED_EXTENSIONS))
    parser.add_argument("--chunk_size", type=int)
    parser.add_argument("--chunk_overlap", type=int)
    parser.add_argument("--output_title_chunk", type=str)
    parser.add_argument("--output_summary_chunk", type=str, default=None)
    parser.add_argument("--data_source_url", type=str, required=False)
    parser.add_argument("--document_path_replacement_regex", type=str, required=False)
    parser.add_argument("--max_sample_files", type=int, default=-1)
    parser.add_argument("--include_summary", type=str, default="False")
    parser.add_argument("--summary_model_config", type=str, default='{"type": "azure_open_ai", "model_name": "gpt-35-turbo", "deployment_name": "gpt-35-turbo"}')
    parser.add_argument("--openai_api_version", type=str, default='2023-03-15-preview')
    parser.add_argument("--openai_api_type", type=str, default=None)
    parser.add_argument("--use_rcts", type=str2bool, default=True)
    parser.add_argument("--output_format", type=str, default="csv")

    args = parser.parse_args()
    print('\n'.join(f'{k}={v}' for k, v in vars(args).items()))

    enable_stdout_logging()
    enable_appinsights_logging()

    try:
        main_wrapper(args, logger)
    finally:
        if _logger_factory.appinsights:
            _logger_factory.appinsights.flush()
            time.sleep(5)
