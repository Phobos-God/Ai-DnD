from __future__ import annotations

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class StoryLogEntryBase(BaseModel):
    content: str


class StoryLogEntryCreate(StoryLogEntryBase):
    pass


class StoryLogEntry(StoryLogEntryBase):
    id: int
    character_id: int
    created_at: datetime