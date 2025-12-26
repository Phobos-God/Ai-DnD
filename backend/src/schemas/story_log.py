from pydantic import BaseModel
from datetime import datetime

# Shared properties
class StoryLogEntryBase(BaseModel):
    content: str
    character_id: int

# Properties to receive via API on creation
class StoryLogEntryCreate(StoryLogEntryBase):
    pass

# Properties to receive via API on update
# Usually, story log entries are append-only, so updates might not be needed
class StoryLogEntryUpdate(BaseModel):
    content: str

# Additional properties stored in DB
class StoryLogEntryInDB(StoryLogEntryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Properties to return via API
class StoryLogEntry(StoryLogEntryInDB):
    pass
