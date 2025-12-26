from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Shared properties
class PartyBase(BaseModel):
    name: str
    description: Optional[str] = None
    leader_id: int

# Properties to receive via API on creation
class PartyCreate(PartyBase):
    pass

# Properties to receive via API on update
class PartyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    leader_id: Optional[int] = None

# Additional properties stored in DB
class PartyInDB(PartyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Properties to return via API
class Party(PartyInDB):
    # Optionally include member IDs or simplified member details here if needed
    # members: List[int] # This would require handling the many-to-many relationship differently
    pass
