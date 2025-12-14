from __future__ import annotations

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class PartyBase(BaseModel):
    name: str
    description: Optional[str] = None


class PartyCreate(PartyBase):
    pass


class Party(PartyBase):
    id: int
    leader_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PartyMemberBase(BaseModel):
    party_id: int
    character_id: int


class PartyMemberCreate(PartyMemberBase):
    pass