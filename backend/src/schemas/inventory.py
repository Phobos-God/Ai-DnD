from __future__ import annotations

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class InventoryItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    quantity: int = 1
    weight: float = 0.0
    value: int = 0


class InventoryItemCreate(InventoryItemBase):
    pass


class InventoryItem(InventoryItemBase):
    id: int
    character_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True