from __future__ import annotations

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CharacterActionBase(BaseModel):
    action_type: str
    target: Optional[str] = None
    roll_result: Optional[int] = None
    modifier: int = 0
    total: Optional[int] = None
    description: Optional[str] = None


class CharacterActionCreate(CharacterActionBase):
    pass


class CharacterAction(CharacterActionBase):
    id: int
    character_id: int
    created_at: datetime