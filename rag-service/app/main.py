from fastapi import FastAPI, HTTPException, Query
from typing import List, Dict
import logging
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Импорты после настройки логирования
import yaml
from minio import Minio

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

@app.on_event("startup")
async def startup_event():
    """Инициализация сервиса при старте"""
    global vectorstore_manager
    
    config = load_config()
    
    # Инициализация MinIO клиента
    minio_client = Minio(
        os.getenv("MINIO_ENDPOINT", config['minio']['endpoint']),
        access_key=os.getenv("MINIO_ACCESS_KEY"),
        secret_key=os.getenv("MINIO_SECRET_KEY"),
        secure=False
    )
    
    bucket_name = os.getenv("MINIO_BUCKET", config['minio']['bucket'])
    
    # Проверка существования бакета
    if not minio_client.bucket_exists(bucket_name):
        raise Exception(f"Bucket {bucket_name} does not exist")
    
    # Инициализация загрузчика PDF
    # Локальные PDF файлы для тестирования при первом запуске
    local_pdfs_dir = "/app/dnd-books"
    
    # Если MinIO недоступен или бакет пуст, используем локальные PDF
    try:
        objects = minio_client.list_objects(bucket_name, recursive=True)
        has_files = any(True for _ in objects)  # Проверяем, есть ли файлы
        
        if not has_files:
            logger.warning(f"Bucket {bucket_name} is empty, using local PDFs from {local_pdfs_dir}")
            pdf_loader = PDFLoader.from_local_directory(local_pdfs_dir, bucket_name)
        else:
            logger.info(f"Using MinIO bucket {bucket_name} for PDF files")
            pdf_loader = PDFLoader(minio_client, bucket_name)
            
    except Exception as e:
        logger.error(f"MinIO connection failed: {e}, using local PDFs")
        pdf_loader = PDFLoader.from_local_directory(local_pdfs_dir, bucket_name)
    
    # Инициализация векторного хранилища
    persist_directory = config['vectorstore']['path']
    collection_name = config['vectorstore']['collection_name']
    vectorstore_manager = VectorStoreManager(persist_directory, collection_name)
    
    # Проверка, пусто ли векторное хранилище
    collection = vectorstore_manager.client.get_collection(collection_name)
    if collection.count() == 0:
        logger.info("Vectorstore is empty. Starting indexing process...")
        
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
                logger.error(f"Error processing book {book['name']}: {e}")
                continue
        
        logger.info(f"Indexing completed. Added {total_docs} documents to vectorstore")
    else:
        logger.info(f"Vectorstore already contains {collection.count()} documents. Skipping indexing.")

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