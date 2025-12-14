from __future__ import annotations

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


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


class CharacterCreate(CharacterBase):
    pass


class Character(CharacterBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True