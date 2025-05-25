from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class ChatSessionCreate(BaseModel):
    user_id: str
    title: Optional[str] = "Untitled"


class ChatSessionUpdate(BaseModel):
    title: Optional[str]
    is_favorite: Optional[bool]


class ChatSessionOut(BaseModel):
    id: UUID
    user_id: str
    title: str
    is_favorite: bool
    created_at: datetime

    class config:
        orm_mode = True
