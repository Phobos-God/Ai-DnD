from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Shared properties
class InventoryItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    quantity: int = 1
    weight: float = 0.0
    value: int = 0  # стоимость в золотых монетах
    character_id: int

# Properties to receive via API on creation
class InventoryItemCreate(InventoryItemBase):
    pass

# Properties to receive via API on update
class InventoryItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[int] = None
    weight: Optional[float] = None
    value: Optional[int] = None
    character_id: Optional[int] = None

# Additional properties stored in DB
class InventoryItemInDB(InventoryItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Properties to return via API
class InventoryItem(InventoryItemInDB):
    pass
