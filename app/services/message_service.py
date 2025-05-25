from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from app.db.models.chat_message import ChatMessage
from app.schemas.message import ChatMessageCreate


async def add_messages(
    db: AsyncSession, message_data: ChatMessageCreate
) -> ChatMessage:
    new_msg = ChatMessage(**message_data.dict())
    db.add(new_msg)
    await db.commit()
    await db.refresh(new_msg)
    return new_msg


async def get_message_by_session(
    db: AsyncSession, session_id: UUID, limit: int = 20, offset: int = 0
):
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at)
        .limit(limit)
        .offset(offset)
    )

    return result.scalars().all()
