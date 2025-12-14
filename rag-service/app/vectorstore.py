import os
import logging
from typing import List

import torch
import chromadb
from chromadb.config import Settings
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

logger = logging.getLogger(__name__)

class VectorStoreManager:
    def __init__(self, persist_directory: str, collection_name: str = "dnd_rules"):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        # Определение устройства для вычислений
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {device}")
        
        self.embedding_function = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": device}
        )
        self.vectorstore = None
        self._initialize_vectorstore()

    def _initialize_vectorstore(self):
        """Инициализация Chroma DB с поддержкой сохранения"""
        chroma_settings = Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=self.persist_directory,
            anonymized_telemetry=False
        )

        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=chroma_settings
        )

        self.vectorstore = Chroma(
            client=self.client,
            collection_name=self.collection_name,
            embedding_function=self.embedding_function
        )
        logger.info(f"Vectorstore initialized at {self.persist_directory}")

    def add_documents(self, documents: List[dict]):
        """Добавление документов в векторное хранилище"""
        texts = [doc["text"] for doc in documents]
        metadatas = [doc.get("metadata", {}) for doc in documents]
        
        self.vectorstore.add_texts(
            texts=texts,
            metadatas=metadatas
        )
        logger.info(f"Added {len(documents)} documents to vectorstore")

    def similarity_search(self, query: str, k: int = 3) -> List[dict]:
        """Поиск релевантных фрагментов"""
        results = self.vectorstore.similarity_search(query, k=k)
        return [
            {
                "text": doc.page_content,
                "metadata": doc.metadata
            } for doc in results
        ]
    
    def get_relevant_context(self, query: str, k: int = 3) -> List[str]:
        """Получение только текстового контекста"""
        results = self.similarity_search(query, k)
        return [item["text"] for item in results]