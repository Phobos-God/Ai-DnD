from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Annotated

from .. import models
from .. import schemas
from ..schemas.character import Character, CharacterCreate
from ..database import SessionLocal, get_db

router = APIRouter(
    prefix="/characters",
    tags=["characters"]
)

@router.get("/", response_model=List[Character])
def get_characters(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    characters = db.query(models.Character).offset(skip).limit(limit).all()
    return characters

@router.get("/{character_id}", response_model=Character)
def get_character(character_id: int, db: Session = Depends(get_db)):
    character = db.query(models.Character).filter(models.Character.id == character_id).first()
    if character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return character

@router.post("/", response_model=Character)
def create_character(
    character: CharacterCreate, 
    db: Session = Depends(get_db)
):
    db_character = models.Character(**character.dict())
    db.add(db_character)
    db.commit()
    db.refresh(db_character)
    return db_character

@router.put("/{character_id}", response_model=Character)
def update_character(
    character_id: int, 
    character: CharacterCreate, 
    db: Session = Depends(get_db)
):
    db_character = db.query(models.Character).filter(models.Character.id == character_id).first()
    if db_character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    
    for key, value in character.dict().items():
        setattr(db_character, key, value)
    
    db.commit()
    db.refresh(db_character)
    return db_character

@router.delete("/{character_id}")
def delete_character(character_id: int, db: Session = Depends(get_db)):
    character = db.query(models.Character).filter(models.Character.id == character_id).first()
    if character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    
    db.delete(character)
    db.commit()
    return {"message": "Character deleted successfully"}