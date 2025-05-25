from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class ChatMessageCreate(BaseModel):
    session_id: UUID
    sender: str
    content: str
    context: Optional[str]
    created_at: datetime

    class config:
        orm_mode = True
