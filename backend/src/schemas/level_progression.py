from __future__ import annotations

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class LevelProgressionBase(BaseModel):
    level: int
    experience_required: int
    abilities_unlocked: Optional[str] = None


class LevelProgressionCreate(LevelProgressionBase):
    pass


class LevelProgression(LevelProgressionBase):
    id: int
    character_id: int
    created_at: datetime