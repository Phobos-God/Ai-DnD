from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Annotated

from .. import schemas, models, database

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix="/characters",
    tags=["characters"]
)

@router.get("/", response_model=List[schemas.Character])
def get_characters(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    characters = db.query(models.Character).offset(skip).limit(limit).all()
    return characters

@router.get("/{character_id}", response_model=schemas.Character)
def get_character(character_id: int, db: Session = Depends(get_db)):
    character = db.query(models.Character).filter(models.Character.id == character_id).first()
    if character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return character

@router.post("/", response_model=schemas.Character)
def create_character(
    character: schemas.CharacterCreate, 
    db: Session = Depends(get_db)
):
    db_character = models.Character(**character.dict())
    db.add(db_character)
    db.commit()
    db.refresh(db_character)
    return db_character

@router.put("/{character_id}", response_model=schemas.Character)
def update_character(
    character_id: int, 
    character: schemas.CharacterCreate, 
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