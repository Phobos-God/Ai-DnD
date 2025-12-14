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
    prefix="/parties",
    tags=["parties"]
)

@router.get("/", response_model=List[schemas.Party])
def get_parties(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    parties = db.query(models.Party).offset(skip).limit(limit).all()
    return parties

@router.get("/{party_id}", response_model=schemas.Party)
def get_party(party_id: int, db: Session = Depends(get_db)):
    party = db.query(models.Party).filter(models.Party.id == party_id).first()
    if party is None:
        raise HTTPException(status_code=404, detail="Party not found")
    return party

@router.post("/", response_model=schemas.Party)
def create_party(
    party: schemas.PartyCreate, 
    db: Session = Depends(get_db)
):
    db_party = models.Party(**party.dict())
    db.add(db_party)
    db.commit()
    db.refresh(db_party)
    return db_party

@router.put("/{party_id}", response_model=schemas.Party)
def update_party(
    party_id: int, 
    party: schemas.PartyCreate, 
    db: Session = Depends(get_db)
):
    db_party = db.query(models.Party).filter(models.Party.id == party_id).first()
    if db_party is None:
        raise HTTPException(status_code=404, detail="Party not found")
    
    for key, value in party.dict().items():
        setattr(db_party, key, value)
    
    db.commit()
    db.refresh(db_party)
    return db_party

@router.delete("/{party_id}")
def delete_party(party_id: int, db: Session = Depends(get_db)):
    party = db.query(models.Party).filter(models.Party.id == party_id).first()
    if party is None:
        raise HTTPException(status_code=404, detail="Party not found")
    
    db.delete(party)
    db.commit()
    return {"message": "Party deleted successfully"}