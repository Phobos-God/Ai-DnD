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
    prefix="/level_progression",
    tags=["level_progression"]
)

@router.get("/", response_model=List[schemas.LevelProgression])
def get_level_progression(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    progression = db.query(models.LevelProgression).offset(skip).limit(limit).all()
    return progression

@router.get("/{entry_id}", response_model=schemas.LevelProgression)
def get_level_progression_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.LevelProgression).filter(models.LevelProgression.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Level progression entry not found")
    return entry

@router.post("/", response_model=schemas.LevelProgression)
def create_level_progression_entry(
    entry: schemas.LevelProgressionCreate, 
    db: Session = Depends(get_db)
):
    db_entry = models.LevelProgression(**entry.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.delete("/{entry_id}")
def delete_level_progression_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.LevelProgression).filter(models.LevelProgression.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Level progression entry not found")
    
    db.delete(entry)
    db.commit()
    return {"message": "Level progression entry deleted successfully"}