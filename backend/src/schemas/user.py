from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# --- Схемы для пользователя ---

# Базовая схема пользователя (общие поля)
class UserBase(BaseModel):
    username: str
    email: EmailStr

# Схема для создания пользователя (включает пароль)
class UserCreate(UserBase):
    password: str

# Схема для обновления пользователя (пароль опционален)
class UserUpdate(UserBase):
    password: Optional[str] = None
    is_active: Optional[bool] = None

# Схема пользователя, возвращаемая из БД (включает ID, хешированный пароль и даты)
class UserInDB(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True # Используется для SQLAlchemy

# Схема пользователя, возвращаемая через API (публичная информация)
class User(UserInDB):
    pass # Может быть расширена позже, если нужно скрыть поля

# --- Схема для входа (логина) ---
class UserLogin(BaseModel):
    username: str
    password: str

# --- Схема для JWT токена ---
class Token(BaseModel):
    access_token: str
    token_type: str

# --- Дополнительная схема для данных токена (опционально, но часто используется) ---
class TokenData(BaseModel):
    username: Optional[str] = None
