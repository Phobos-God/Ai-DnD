import os
import logging
from typing import List, Dict
from dataclasses import dataclass

import PyPDF2
import yaml
from minio import Minio
from minio.error import S3Error

# Tokenizer для чанкинга
from transformers import AutoTokenizer

logger = logging.getLogger(__name__)

_TOKENIZER = None

def get_tokenizer():
    global _TOKENIZER
    if _TOKENIZER is None:
        _TOKENIZER = AutoTokenizer.from_pretrained(
            "/app/models/paraphrase-multilingual-MiniLM-L12-v2",
            use_fast=True
        )
    return _TOKENIZER

@dataclass
class Document:
    text: str
    metadata: Dict


class PDFLoader:

    def __init__(self, minio_client: Minio, bucket_name: str):
        self.minio_client = minio_client
        self.bucket_name = bucket_name
        
    @classmethod
    def from_local_directory(cls, local_dir: str, bucket_name: str):
        """Создание загрузчика, который читает PDF из локальной директории"""
        # Создаем фиктивный MinIO клиент
        loader = cls(None, bucket_name)
        loader.local_dir = local_dir
        return loader
        
    def _use_local_pdf(self, object_name: str) -> str:
        """Получение пути к локальному PDF файлу"""
        local_path = os.path.join(self.local_dir, object_name)
        if os.path.exists(local_path):
            return local_path
        else:
            raise FileNotFoundError(f"Local PDF not found: {local_path}")

    def _download_pdf(self, object_name: str, download_path: str) -> str:
        """Скачивание PDF из MinIO или использование локального файла"""
        try:
            if hasattr(self, 'local_dir') and self.local_dir:
                # Используем локальный файл
                local_path = self._use_local_pdf(object_name)
                # Копируем в временный путь
                import shutil
                shutil.copy2(local_path, download_path)
                logger.info(f"Used local PDF {local_path} -> {download_path}")
                return download_path
            else:
                # Используем MinIO
                self.minio_client.fget_object(
                    self.bucket_name, object_name, download_path
                )
                logger.info(f"Downloaded {object_name} from MinIO to {download_path}")
                return download_path
                
        except Exception as e:
            logger.error(f"Error accessing PDF {object_name}: {e}")
            raise

    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """Извлечение текста из PDF"""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF {pdf_path}: {e}")
            raise



    def _split_text_by_tokens(self, text: str, chunk_size: int = 384, chunk_overlap: int = 64) -> List[str]:
        """
        Token-based chunking using the model's tokenizer.
        Ensures chunks do not exceed model's token limit (512),
        with safety margin.
        """
        
        tokenizer = get_tokenizer()
        tokens = tokenizer.encode(
            text,
            add_special_tokens=False  # Без [CLS], [SEP]
        )
        
        chunks = []
        start = 0
        
        while start < len(tokens):
            end = start + chunk_size
            chunk_tokens = tokens[start:end]
            
            # Декодируем обратно в текст
            chunk_text = tokenizer.decode(
                chunk_tokens,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=True
            )
            
            chunks.append(chunk_text)
            
            # Переход с оверлапом
            start = end - chunk_overlap
            if start < 0:
                start = 0
        
        return chunks

    def load_and_chunk_pdf(self, pdf_object_name: str, chunk_size: int = 512, chunk_overlap: int = 64) -> List[Document]:
        """Загрузка, извлечение и чанкинг PDF"""
        # Определяем путь для временного файла
        filename = os.path.basename(pdf_object_name)
        temp_path = f"/tmp/{filename}"
        
        try:
            # Скачиваем PDF
            self._download_pdf(pdf_object_name, temp_path)
            
            # Извлекаем текст
            text = self._extract_text_from_pdf(temp_path)
            
            # Разбиваем на чанки
            chunks = self._split_text_by_tokens(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            
            # Создаем документы с метаданными
            documents = []
            for i, chunk in enumerate(chunks):
                doc = Document(
                    text=chunk,
                    metadata={
                        "source": pdf_object_name,
                        "chunk_index": i,
                        "total_chunks": len(chunks)
                    }
                )
                documents.append(doc)
            
            logger.info(f"Created {len(documents)} chunks from {pdf_object_name}")
            return documents
            
        finally:
            # Удаляем временный файл
            if os.path.exists(temp_path):
                os.remove(temp_path)