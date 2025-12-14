from __future__ import annotations

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class DiceRollBase(BaseModel):
    dice_type: str
    roll_result: int
    modifier: int = 0
    total: int
    description: Optional[str] = None


class DiceRollCreate(DiceRollBase):
    pass


class DiceRoll(DiceRollBase):
    id: int
    character_id: int
    created_at: datetime