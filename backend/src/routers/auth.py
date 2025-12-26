from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
# Используем относительные импорты, как в других роутерах
from .. import models, security
from ..database import SessionLocal, get_db
# Импортируем схемы напрямую из подмодуля
from ..schemas.user import User as UserSchema, UserCreate as UserCreateSchema, UserLogin as UserLoginSchema, Token as TokenSchema
from ..models import User as UserModel
from ..database import SessionLocal

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

def get_db():
    db = SessionLocal() # Используем SessionLocal из относительного импорта
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserSchema) # Используем напрямую импортированную схему
def register_user(user: UserCreateSchema, db: Session = Depends(get_db)): # Используем UserCreateSchema
    # Проверка существования пользователя по имени
    db_user_by_username = db.query(UserModel).filter(UserModel.username == user.username).first() # Используем UserModel
    if db_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    # Проверка существования пользователя по email
    db_user_by_email = db.query(UserModel).filter(UserModel.email == user.email).first() # Используем UserModel
    if db_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Хеширование пароля
    hashed_password = security.get_password_hash(user.password) # Используем security

    # Создание нового пользователя
    db_user = UserModel( # Используем UserModel
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=TokenSchema) # Используем напрямую импортированную схему токена
def login_user(form_data: Annotated[UserLoginSchema, Depends()], db: Session = Depends(get_db)): # Используем UserLoginSchema
    # Поиск пользователя по имени
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first() # Используем UserModel
    if not user or not security.verify_password(form_data.password, user.hashed_password): # Используем security
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Создание JWT токена
    access_token = security.create_access_token(data={"sub": user.username}) # Используем security
    return {"access_token": access_token, "token_type": "bearer"}
