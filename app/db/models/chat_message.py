import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Enum, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from enum import Enum as PyEnum
from app.db.base import Base


class senderEnum(PyEnum):
    user = "user"
    assistant = "assistant"


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(
        UUID(as_uuid=True), ForeignKey("chat_sessions.id", ondelete="CASCADE")
    )
    sender = Column(Enum(senderEnum), nullable=False)
    content = Column(Text, nullable=False)
    context = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    session = relationship("ChatSession", back_populates="messages")
