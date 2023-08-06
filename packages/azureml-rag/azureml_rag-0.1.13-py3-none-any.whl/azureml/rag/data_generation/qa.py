# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Question-Answer Data Generator."""
import glob
import os
import time
import traceback
from collections import Counter, defaultdict
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from logging import Logger, getLogger
from typing import Dict, List, Tuple

import bs4
import pandas as pd
import tiktoken
from azureml.rag.models import init_llm
from langchain.chains.llm import LLMChain
from langchain.llms.base import BaseLLM
from langchain.prompts.prompt import PromptTemplate

_MODULE_DIR = os.path.dirname(os.path.abspath(__file__))


class QAType(str, Enum):
    """QAType defines different QA types available."""

    SHORT_ANSWER = "SHORT_ANSWER"
    LONG_ANSWER = "LONG_ANSWER"
    BOOLEAN = "BOOLEAN"
    SUMMARY = "SUMMARY"


@dataclass
class Chunk:
    """Chunk represents a chunk inside a file produced by crack_and_chunk."""

    text: str
    source: str
    qa_type: QAType


class QADataGenerator:
    """Class for generating Question-Answer data for any texts."""

    _MIN_CHUNK_TOKEN_COUNT = 20
    _MAX_CHUNK_TOKEN_COUNT = 1200  # keeping it well under 2049 - max tokens for gpt-3 models: https://platform.openai.com/docs/models/gpt-3
    _PROMPTS_DIR = os.path.join(_MODULE_DIR, "prompts")
    _PROMPT_FILENAME = {
        QAType.SHORT_ANSWER: "prompt_qa_short_answer.txt",
        QAType.LONG_ANSWER: "prompt_qa_long_answer.txt",
        QAType.BOOLEAN: "prompt_qa_boolean.txt",
        QAType.SUMMARY: "prompt_qa_summary.txt",
    }
    _MAX_PARSING_FAILURE_COUNT = 10  # after these many parsing failures, exception is re-raised
    _SORTED_COLUMNS = ["qaType", "question", "answer", "subContext", "title", "source", "context"]
    _SUMMARY_QUESTION = "Write a summary in less than %d words for: %s"
    _SUMMARY_NUM_OF_WORDS = 50

    def __init__(self, model_config: Dict[str, str], logger: Logger, activity_logger: Logger):
        """Initialize a QA data generator using LLM model defined by model_config."""
        self.model_config = model_config
        self.logger = logger or getLogger("QADataGenerator")
        self.activity_logger = activity_logger or self.logger
        self.llm: BaseLLM = init_llm(model_config)
        self.llm_chains: Dict[QAType, LLMChain] = {}
        for qa_type in QAType:
            self.llm_chains[qa_type] = LLMChain(prompt=self._get_prompt_template(qa_type), llm=self.llm)
        self._parsing_failure_count = None  # tracks parsing failures for a generate() call

    @lru_cache
    def _encoding_for_model(self) -> tiktoken.Encoding:
        prefixes = ["gpt-35-turbo", "gpt-3.5-turbo", "gpt-4"]
        model = self.model_config["model"]
        if any([model.startswith(prefix) for prefix in prefixes]):
            encoding_name = "cl100k_base"
        else:
            encoding_name = "gpt2"
        return tiktoken.get_encoding(encoding_name)

    def _get_tokens(self, text) -> List[int]:
        return self._encoding_for_model().encode(text)

    def _get_text(self, tokens) -> str:
        return self._encoding_for_model().decode(tokens)

    def _chunk_batches(self, input_dir, batch_size: int) -> List[Chunk]:
        glob_path = os.path.join(input_dir, "**", "*")
        files = glob.glob(glob_path, recursive=True)
        files = [file for file in files if os.path.isfile(file)]
        self.activity_logger.info(f"Reading {batch_size} chunks at a time from {len(files)} files")

        qa_type_assigner = self._qa_type_assigner()
        batch = []
        for filepath in files:
            filename = os.path.basename(filepath)
            file_df = pd.read_csv(filepath)
            for i, chunk_text in enumerate(file_df["Chunk"]):
                self.logger.info(f"Read chunk: source:{filename} chunk:{i}")
                chunk = Chunk(text=chunk_text, source=filename, qa_type=next(qa_type_assigner))
                batch.append(chunk)
                if len(batch) == batch_size:
                    yield batch
                    batch = []
        yield batch

    def _get_num_of_questions(self, num_of_tokens) -> int:
        # Determine the number of QA pairs that can be generated for a chunk text.
        # Approximation: 100 tokens has enough details for 1 QA pair.
        # Ceiling of max 10 QA pairs to avoid truncated xml output.
        return min(num_of_tokens // 100, 10)

    def _get_prompt_template(self, qa_type: QAType) -> PromptTemplate:
        self.logger.info(f"Getting prompt template for {qa_type} QA type")
        filename = self._PROMPT_FILENAME[qa_type]
        filepath = os.path.join(self._PROMPTS_DIR, filename)
        with open(filepath) as f:
            template = f.read()
        if qa_type == QAType.SUMMARY:
            return PromptTemplate(template=template, input_variables=["text", "num_of_words"])
        return PromptTemplate(template=template, input_variables=["text", "num_of_questions"])

    def _qa_type_assigner(self) -> QAType:
        """Yields QATypes in round-robin fashion."""
        lst = list(QAType)
        i = 0
        while True:
            yield lst[i]
            if i == len(lst) - 1:
                i = 0
            else:
                i += 1

    def _parse_response(self, response_text: str, qa_type: QAType) -> Tuple[str, List]:
        root_index = response_text.find("<Root>")
        response_text = response_text[root_index:]
        response_text = response_text.rstrip().rstrip("```")
        # using lxml instead of xml since it's lenient during parsing. ex. "<=" and "&" fail for xml
        soup = bs4.BeautifulSoup(response_text, "lxml")
        title = soup.find("title").get_text()
        qa_list = []
        if qa_type == QAType.SUMMARY:
            question = self._SUMMARY_QUESTION % (self._SUMMARY_NUM_OF_WORDS, title)
            answer = soup.find("summary").get_text()
            qa_list.append((question, answer, ""))
        else:
            invalid_qa_count = 0
            qas_elem = soup.find("qas")
            qas_children: List[bs4.Tag] = qas_elem.findChildren("qa", recursive=False)
            for qa in qas_children:
                question = qa.find("q").get_text()
                answer = qa.find("a").get_text()
                if qa_type == QAType.SHORT_ANSWER and len(answer.split()) > 10:  # answer must be short
                    self.logger.warn(f"Invalid {qa_type} answer: {answer}")
                    invalid_qa_count += 1
                    continue
                if qa_type == QAType.BOOLEAN and answer not in ["True", "False"]:
                    self.logger.warn(f"Invalid {qa_type} answer: {answer}")
                    invalid_qa_count += 1
                    continue
                verbatim_elem = qa.find("verbatimsentence")
                if verbatim_elem:
                    verbatim = verbatim_elem.get_text()
                else:
                    verbatim = ""
                qa_list.append((question, answer, verbatim))
            if invalid_qa_count > 0:
                self.activity_logger.warn(f"Ignored {invalid_qa_count} invalid QAs for {qa_type}")
        return title, qa_list

    def _parse_and_add_questions(self, result_dict: Dict[str, List], response_text: str, chunk: Chunk) -> Dict[str, List]:
        qa_list = []
        try:
            title, qa_list = self._parse_response(response_text, chunk.qa_type)
        except Exception:
            self.logger.info(f"Parsing failed for chunk source:{chunk.source} response_text:\n{response_text}\n")
            if self._parsing_failure_count is not None:
                self._parsing_failure_count -= 1
                if self._parsing_failure_count <= 0:
                    raise
                self.activity_logger.warn(f"Ignoring parsing failure:\n{traceback.format_exc()}")
        for question, answer, verbatim in qa_list:
            result_dict["qaType"].append(chunk.qa_type.value)
            result_dict["question"].append(question)
            result_dict["answer"].append(answer)
            result_dict["subContext"].append(verbatim)
            result_dict["title"].append(title)
            result_dict["source"].append(chunk.source)
            result_dict["context"].append(chunk.text)
        return result_dict

    def generate_for_chunks(self, chunks: List[Chunk], total_questions: int = None) -> Tuple[pd.DataFrame, Dict]:
        """Generate QA data using texts from chunks. total_questions (optional) can be passed to cap the number of QAs to generate."""
        prompts, prompt_chunks = [], []
        question_count = 0
        self.logger.info(f"Preparing prompts from {len(chunks)} chunks")
        for chunk in chunks:
            if total_questions is not None and question_count >= total_questions:
                self.logger.info(f"Ignoring remaining chunks after collecting chunks required for {total_questions} questions")
                break

            tokens = self._get_tokens(chunk.text)
            if len(tokens) <= self._MIN_CHUNK_TOKEN_COUNT:
                self.logger.warn(
                    f"Ignoring chunk from source:{chunk.source} as num_of_tokens ({len(tokens)}) is less than min token count ({self._MIN_CHUNK_TOKEN_COUNT})")
                continue
            if len(tokens) >= self._MAX_CHUNK_TOKEN_COUNT:
                self.logger.warn(
                    f"Truncating chunk from source:{chunk.source} as num_of_tokens ({len(tokens)}) is greater than max token count ({self._MAX_CHUNK_TOKEN_COUNT})")
                tokens = tokens[:self._MAX_CHUNK_TOKEN_COUNT]
                chunk.text = self._get_text(tokens)

            input_vars = dict(text=chunk.text)
            if chunk.qa_type == QAType.SUMMARY:
                input_vars["num_of_words"] = self._SUMMARY_NUM_OF_WORDS
                question_count += 1
            else:
                input_vars["num_of_questions"] = self._get_num_of_questions(len(tokens))
                question_count += input_vars["num_of_questions"]
            prep_prompts, _ = self.llm_chains[chunk.qa_type].prep_prompts([input_vars])
            prompts.append(prep_prompts[0])
            prompt_chunks.append(chunk)

        self.logger.info(f"Calling LLM for {len(prompts)} prompts...")
        start_time = time.time()
        response = self.llm.generate_prompt(prompts)  # call is parallelized across prompts
        self.logger.info(f"LLM call completed in {time.time()-start_time} secs")

        result_dict = defaultdict(list)
        for i, generation in enumerate(response.generations):
            response_text = generation[0].text
            chunk = prompt_chunks[i]
            result_dict = self._parse_and_add_questions(result_dict, response_text, chunk)
        qa_data_df = pd.DataFrame(result_dict, columns=self._SORTED_COLUMNS)
        return qa_data_df, response.llm_output["token_usage"]

    def generate(self, input_dir: str, total_questions: int, chunk_batch_size: int = 10) -> Tuple[pd.DataFrame, Dict]:
        """Generate QA data by first loading chunks from input_dir, and then calling `generate_for_chunks()` for a batch of chunk_batch_size.
        total_questions must be passed to cap the number of QAs to generate."""
        token_usage = Counter()
        qa_data_df = pd.DataFrame(columns=self._SORTED_COLUMNS)
        self._parsing_failure_count = 0
        try:
            for chunk_batch in self._chunk_batches(input_dir, chunk_batch_size):
                chunks_qa_data_df, token_usage_chunks = self.generate_for_chunks(chunk_batch)
                qa_data_df = pd.concat([qa_data_df, chunks_qa_data_df], ignore_index=True)
                token_usage += token_usage_chunks
                if len(qa_data_df.index) >= total_questions:
                    break
        except (Exception, KeyboardInterrupt) as e:
            e.qa_data_df = qa_data_df  # save whatever partial result we have so far
            e.token_usage = token_usage
            raise
        finally:
            self._parsing_failure_count = None
        return qa_data_df, token_usage
