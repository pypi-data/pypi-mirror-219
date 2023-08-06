# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""MLIndex class for interacting with MLIndex assets."""
from azureml.rag.documents import Document, DocumentChunksIterator
from azureml.rag.embeddings import EmbeddingsContainer
from azureml.rag.utils.connections import get_connection_credential
from azureml.rag.utils.logging import get_logger
from enum import Enum
from langchain.document_loaders.base import BaseLoader
from langchain.schema import Document as LangChainDocument
from pathlib import Path
import tempfile
from typing import Any, Dict, Iterable, Iterator, List, Optional, Union
import yaml


logger = get_logger('mlindex')


class MLIndex:
    """MLIndex class for interacting with MLIndex assets."""
    base_uri: str
    index_config: dict
    embeddings_config: dict

    _underlying_index: Any = None

    def __init__(self, uri: Optional[Union[str, object]] = None, mlindex_config: Optional[dict] = None):
        """Initialize MLIndex from a URI or AzureML Data Asset"""
        if uri is not None:
            if isinstance(uri, str):
                uri = str(uri)
            else:
                # Assume given AzureML Data Asset
                uri = uri.path
            try:
                import fsspec
            except ImportError:
                raise ValueError(
                    "Could not import fsspec python package. "
                    "Please install it with `pip install fsspec`."
                )
            try:
                import azureml.fsspec
            except ImportError:
                raise ValueError(
                    "Could not import azureml-fsspec python package. "
                    "Please install it with `pip install azureml-fsspec`."
                )

            self.base_uri = uri

            mlindex_config = None
            try:
                mlindex_file = fsspec.open(f"{uri.rstrip('/')}/MLIndex", 'r')
                # parse yaml to dict
                with mlindex_file as f:
                    mlindex_config = yaml.safe_load(f)
            except Exception as e:
                raise ValueError(f"Could not find MLIndex: {e}") from e
        elif mlindex_config is None:
            raise ValueError("Must provide either uri or mlindex_config")

        self.index_config = mlindex_config.get('index', {})
        if self.index_config is None:
            raise ValueError("Could not find index config in MLIndex yaml")
        self.embeddings_config = mlindex_config.get('embeddings', {})
        if self.embeddings_config is None:
            raise ValueError("Could not find embeddings config in MLIndex yaml")

    @property
    def name(self) -> str:
        """Returns the name of the MLIndex."""
        return self.index_config.get('name', '')

    @name.setter
    def name(self, value: str):
        """Sets the name of the MLIndex."""
        self.index_config['name'] = value

    @property
    def description(self) -> str:
        """Returns the description of the MLIndex."""
        return self.index_config.get('description', '')

    @description.setter
    def description(self, value: str):
        """Sets the description of the MLIndex."""
        self.index_config['description'] = value

    def get_langchain_embeddings(self):
        """Get the LangChainEmbeddings from the MLIndex"""
        embeddings = EmbeddingsContainer.from_metadata(self.embeddings_config)

        return embeddings.as_langchain_embeddings()

    def as_langchain_vectorstore(self):
        """Converts MLIndex to a retriever object that can be used with langchain, may download files."""
        index_kind = self.index_config.get('kind', None)
        if index_kind == 'acs':
            from azureml.rag.langchain.acs import AzureCognitiveSearchVectorStore

            credential = get_connection_credential(self.index_config)

            return AzureCognitiveSearchVectorStore(
                index_name=self.index_config.get('index'),
                endpoint=self.index_config.get('endpoint'),
                embeddings=self.get_langchain_embeddings(),
                field_mapping=self.index_config.get('field_mapping', {}),
                credential=credential,
            )
        elif index_kind == 'faiss':
            from fsspec.core import url_to_fs
            from langchain.vectorstores.faiss import FAISS

            embeddings = EmbeddingsContainer.from_metadata(self.embeddings_config).as_langchain_embeddings()

            fs, uri = url_to_fs(self.base_uri)

            with tempfile.TemporaryDirectory() as tmpdir:
                fs.download(f"{uri.rstrip('/')}/index.pkl", f"{str(tmpdir)}")
                fs.download(f"{uri.rstrip('/')}/index.faiss", f"{str(tmpdir)}")
                langchain_faiss = FAISS.load_local(str(tmpdir), embeddings)

            return langchain_faiss
        else:
            raise ValueError(f"Unknown index kind: {index_kind}")

    def as_langchain_retriever(self, **kwargs):
        """Converts MLIndex to a retriever object that can be used with langchain, may download files."""
        index_kind = self.index_config.get('kind', None)
        if index_kind == 'acs':
            return self.as_langchain_vectorstore().as_retriever(**kwargs)
            # from azureml.rag.langchain.acs import AzureCognitiveSearchRetriever

            # credential = get_connection_credential(self.index_config)

            # return AzureCognitiveSearchRetriever(
            #     index_name=self.index_config.get('index'),
            #     endpoint=self.index_config.get('endpoint'),
            #     credential=credential,
            #     top_k=self.index_config.get('top_k', 4),
            # )
        elif index_kind == 'faiss':
            return self.as_langchain_vectorstore().as_retriever()
        else:
            raise ValueError(f"Unknown index kind: {index_kind}")

    def __repr__(self):
        """Returns a string representation of the MLIndex object."""
        return yaml.dump({
            'index': self.index_config,
            'embeddings': self.embeddings_config,
        })
