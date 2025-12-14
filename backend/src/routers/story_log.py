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
    prefix="/story_log",
    tags=["story_log"]
)

@router.get("/", response_model=List[schemas.StoryLogEntry])
def get_story_log_entries(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    entries = db.query(models.StoryLogEntry).offset(skip).limit(limit).all()
    return entries

@router.get("/{entry_id}", response_model=schemas.StoryLogEntry)
def get_story_log_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.StoryLogEntry).filter(models.StoryLogEntry.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Story log entry not found")
    return entry

@router.post("/", response_model=schemas.StoryLogEntry)
def create_story_log_entry(
    entry: schemas.StoryLogEntryCreate, 
    db: Session = Depends(get_db)
):
    db_entry = models.StoryLogEntry(**entry.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.delete("/{entry_id}")
def delete_story_log_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.StoryLogEntry).filter(models.StoryLogEntry.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Story log entry not found")
    
    db.delete(entry)
    db.commit()
    return {"message": "Story log entry deleted successfully"}