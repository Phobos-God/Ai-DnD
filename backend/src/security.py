from datetime import datetime, timedelta, timezone
from typing import Optional
import os
from jose import JWTError, jwt
from passlib.context import CryptContext

# Контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Секретный ключ и алгоритм для JWT (лучше получать из env)
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-it-in-production") # Обязательно смените в продакшене!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет, совпадает ли plain_password с hashed_password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Возвращает хеш для заданного пароля."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Создает JWT токен."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
