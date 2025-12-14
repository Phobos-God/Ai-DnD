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
    prefix="/actions",
    tags=["actions"]
)

@router.get("/", response_model=List[schemas.CharacterAction])
def get_actions(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    actions = db.query(models.CharacterAction).offset(skip).limit(limit).all()
    return actions

@router.get("/{action_id}", response_model=schemas.CharacterAction)
def get_action(action_id: int, db: Session = Depends(get_db)):
    action = db.query(models.CharacterAction).filter(models.CharacterAction.id == action_id).first()
    if action is None:
        raise HTTPException(status_code=404, detail="Action not found")
    return action

@router.post("/", response_model=schemas.CharacterAction)
def create_action(
    action: schemas.CharacterActionCreate, 
    db: Session = Depends(get_db)
):
    db_action = models.CharacterAction(**action.dict())
    db.add(db_action)
    db.commit()
    db.refresh(db_action)
    return db_action

@router.delete("/{action_id}")
def delete_action(action_id: int, db: Session = Depends(get_db)):
    action = db.query(models.CharacterAction).filter(models.CharacterAction.id == action_id).first()
    if action is None:
        raise HTTPException(status_code=404, detail="Action not found")
    
    db.delete(action)
    db.commit()
    return {"message": "Action deleted successfully"}