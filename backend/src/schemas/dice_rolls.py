from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Shared properties
class DiceRollBase(BaseModel):
    dice_type: str  # d4, d6, d8, d10, d12, d20, d100
    roll_result: int
    modifier: int = 0
    total: int
    character_id: int
    description: Optional[str] = None

# Properties to receive via API on creation
class DiceRollCreate(DiceRollBase):
    pass

# Properties to receive via API on update
# Dice rolls are usually immutable once made
class DiceRollUpdate(BaseModel):
    description: Optional[str] = None

# Additional properties stored in DB
class DiceRollInDB(DiceRollBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Properties to return via API
class DiceRoll(DiceRollInDB):
    pass
