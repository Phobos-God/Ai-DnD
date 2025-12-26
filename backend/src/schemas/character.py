from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Shared properties
class CharacterBase(BaseModel):
    name: str
    race: str
    character_class: str
    level: int = 1
    health_points: int = 10
    max_health_points: int = 10
    experience: int = 0
    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10
    gold: int = 0
    description: Optional[str] = None
    image_url: Optional[str] = None
    owner_id: int

# Properties to receive via API on creation
class CharacterCreate(CharacterBase):
    pass

# Properties to receive via API on update
class CharacterUpdate(BaseModel):
    name: Optional[str] = None
    race: Optional[str] = None
    character_class: Optional[str] = None
    level: Optional[int] = None
    health_points: Optional[int] = None
    max_health_points: Optional[int] = None
    experience: Optional[int] = None
    strength: Optional[int] = None
    dexterity: Optional[int] = None
    constitution: Optional[int] = None
    intelligence: Optional[int] = None
    wisdom: Optional[int] = None
    charisma: Optional[int] = None
    gold: Optional[int] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    owner_id: Optional[int] = None

# Additional properties stored in DB
class CharacterInDB(CharacterBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Properties to return via API
class Character(CharacterInDB):
    pass
