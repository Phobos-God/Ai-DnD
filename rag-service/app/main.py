from fastapi import FastAPI, HTTPException, Query
from typing import List, Dict
import logging
import os
import time  # Для задержки в retry

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Импорты после настройки логирования
import yaml
from minio import Minio
from retrying import retry  # Новый импорт для ретраев

from loader import PDFLoader, Document
from vectorstore import VectorStoreManager

app = FastAPI(
    title="RAG Service for AI DnD",
    description="Retrieval-Augmented Generation service for D&D 5e rules",
    version="1.0.0"
)

# Глобальные переменные
vectorstore_manager: VectorStoreManager = None

def load_config():
    """Загрузка конфигурации из config.yaml"""
    config_path = os.getenv("CONFIG_PATH", "/app/config.yaml")
    with open(config_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

# Функция для ретрая операций с MinIO
@retry(stop_max_attempt_number=3, wait_fixed=5000)  # 3 попытки, задержка 5 сек
def check_minio_connection(minio_client, bucket_name):
    """Проверка подключения к MinIO с ретраями"""
    if not minio_client.bucket_exists(bucket_name):
        raise Exception(f"Bucket {bucket_name} does not exist")
    return True

@app.on_event("startup")
async def startup_event():
    """Инициализация сервиса при старте"""
    global vectorstore_manager
    
    try:
        logger.info("Startup event started")
        config = load_config()
        logger.info("Config loaded successfully")
        
        # Инициализация MinIO клиента
        minio_client = Minio(
            os.getenv("MINIO_ENDPOINT", config['minio']['endpoint']),
            access_key=os.getenv("MINIO_ACCESS_KEY"),
            secret_key=os.getenv("MINIO_SECRET_KEY"),
            secure=False
        )
        logger.info("MinIO client created")
        
        bucket_name = os.getenv("MINIO_BUCKET", config['minio']['bucket'])
        
        # Локальные PDF файлы
        local_pdfs_dir = "/app/dnd-books"
        
        try:
            # Проверяем подключение с ретраями
            check_minio_connection(minio_client, bucket_name)
            logger.info("MinIO connection OK, using bucket")
            
            # Если подключение OK, проверяем файлы
            objects = minio_client.list_objects(bucket_name, recursive=True)
            has_files = any(True for _ in objects)  # Проверяем, есть ли файлы
            
            if not has_files:
                logger.warning(f"Bucket {bucket_name} is empty, fallback to local PDFs")
                pdf_loader = PDFLoader.from_local_directory(local_pdfs_dir, bucket_name)
            else:
                logger.info(f"Using MinIO bucket {bucket_name} for PDF files")
                pdf_loader = PDFLoader(minio_client, bucket_name)
                
        except Exception as e:
            logger.warning(f"MinIO failed: {str(e)}, fallback to local")
            # fallback pdf_loader
            pdf_loader = PDFLoader.from_local_directory(local_pdfs_dir, bucket_name)
        
        # Инициализация векторного хранилища
        persist_directory = config['vectorstore']['path']
        collection_name = config['vectorstore']['collection_name']
        vectorstore_manager = VectorStoreManager(persist_directory, collection_name)
        logger.info("Vectorstore manager initialized")
        
        # Проверка, пусто ли векторное хранилище
        collection = vectorstore_manager.client.get_collection(collection_name)
        logger.info(f"Collection count: {collection.count()}")
        
        if collection.count() == 0:
            logger.info("Vectorstore empty, starting indexing...")
            
            # Загрузка и индексация всех книг из конфигурации
            books = config['books']
            total_docs = 0
            
            for book in books:
                pdf_file = book['file']
                logger.info(f"Processing book: {book['name']} ({pdf_file})")
                
                try:
                    # Загрузка и чанкинг PDF
                    documents = pdf_loader.load_and_chunk_pdf(
                        pdf_file,
                        chunk_size=config['pdf']['chunk_size'],
                        chunk_overlap=config['pdf']['chunk_overlap']
                    )
                    
                    # Преобразование в словари для VectorStore
                    docs_dict = [
                        {"text": doc.text, "metadata": doc.metadata} 
                        for doc in documents
                    ]
                    
                    # Добавление в векторное хранилище
                    vectorstore_manager.add_documents(docs_dict)
                    total_docs += len(documents)
                    
                except Exception as e:
                    logger.error(f"Error indexing {book['name']}: {str(e)}")
                    continue
            
            logger.info(f"Indexing completed. Added {total_docs} documents to vectorstore")
        else:
            logger.info(f"Vectorstore already contains {collection.count()} documents. Skipping indexing.")
            
    except Exception as e:
        logger.error(f"Startup event failed: {str(e)}", exc_info=True)  # Full traceback

@app.get("/")
async def root():
    return {"message": "RAG Service for AI DnD is running"}

@app.get("/health")
async def health_check():
    """Проверка работоспособности сервиса"""
    try:
        config = load_config()
        collection = vectorstore_manager.client.get_collection(
            config['vectorstore']['collection_name']
        )
        return {
            "status": "healthy",
            "vectorstore_count": collection.count(),
            "message": "Service is ready to serve requests"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service is not healthy")

@app.get("/retrieve")
async def retrieve(
    query: str = Query(..., description="Поисковый запрос"),
    top_k: int = Query(3, ge=1, le=10, description="Количество возвращаемых результатов")
) -> Dict:
    """
    Извлечение релевантных фрагментов текста на основе запроса
    """
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    try:
        context = vectorstore_manager.get_relevant_context(query, k=top_k)
        
        return {
            "query": query,
            "context": context,
            "sources": list(set([doc["metadata"]["source"] for doc in vectorstore_manager.similarity_search(query, k=top_k)]))
        }
    except Exception as e:
        logger.error(f"Error during retrieval: {e}")
        raise HTTPException(status_code=500, detail="Error during retrieval")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=False)