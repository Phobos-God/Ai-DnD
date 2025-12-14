from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

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

    class Config:
        from_attributes = True

class StoryLogEntryBase(BaseModel):
    content: str

class StoryLogEntryCreate(StoryLogEntryBase):
    pass

class StoryLogEntry(StoryLogEntryBase):
    id: int
    character_id: int
    created_at: datetime

    class Config:
        from_attributes = True

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

    class Config:
        from_attributes = True

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

    class Config:
        from_attributes = True
