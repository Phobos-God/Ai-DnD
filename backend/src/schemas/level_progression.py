from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Shared properties
class LevelProgressionBase(BaseModel):
    character_id: int
    level: int
    experience_required: int
    abilities_unlocked: Optional[str] = None  # JSON или текстовое описание разблокированных способностей

# Properties to receive via API on creation
class LevelProgressionCreate(LevelProgressionBase):
    pass

# Properties to receive via API on update
class LevelProgressionUpdate(BaseModel):
    abilities_unlocked: Optional[str] = None

# Additional properties stored in DB
class LevelProgressionInDB(LevelProgressionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Properties to return via API
class LevelProgression(LevelProgressionInDB):
    pass
