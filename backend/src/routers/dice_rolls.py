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
    prefix="/dice_rolls",
    tags=["dice_rolls"]
)

@router.get("/", response_model=List[schemas.DiceRoll])
def get_dice_rolls(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    rolls = db.query(models.DiceRoll).offset(skip).limit(limit).all()
    return rolls

@router.get("/{roll_id}", response_model=schemas.DiceRoll)
def get_dice_roll(roll_id: int, db: Session = Depends(get_db)):
    roll = db.query(models.DiceRoll).filter(models.DiceRoll.id == roll_id).first()
    if roll is None:
        raise HTTPException(status_code=404, detail="Dice roll not found")
    return roll

@router.post("/", response_model=schemas.DiceRoll)
def create_dice_roll(
    roll: schemas.DiceRollCreate, 
    db: Session = Depends(get_db)
):
    db_roll = models.DiceRoll(**roll.dict())
    db.add(db_roll)
    db.commit()
    db.refresh(db_roll)
    return db_roll

@router.delete("/{roll_id}")
def delete_dice_roll(roll_id: int, db: Session = Depends(get_db)):
    roll = db.query(models.DiceRoll).filter(models.DiceRoll.id == roll_id).first()
    if roll is None:
        raise HTTPException(status_code=404, detail="Dice roll not found")
    
    db.delete(roll)
    db.commit()
    return {"message": "Dice roll deleted successfully"}