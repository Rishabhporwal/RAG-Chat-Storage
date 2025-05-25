from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from fastapi import HTTPException

from app.db.models.chat_message import ChatMessage
from app.schemas.message import ChatMessageCreate
from app.core.logging import logger

MAX_LIMIT = 100  # Limit to prevent heavy DB loads


async def add_messages(
    db: AsyncSession, message_data: ChatMessageCreate
) -> ChatMessage:
    try:
        if not message_data.session_id or not message_data.content:
            raise HTTPException(
                status_code=422, detail="Session ID and content are required."
            )

        new_msg = ChatMessage(**message_data.dict())
        db.add(new_msg)
        await db.commit()
        await db.refresh(new_msg)
        logger.info(f"Message added to session: {new_msg.session_id}")
        return new_msg

    except Exception as e:
        logger.exception(f"Error adding message: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def get_message_by_session(
    db: AsyncSession, session_id: UUID, limit: int = 20, offset: int = 0
):
    if not isinstance(session_id, UUID):
        raise HTTPException(status_code=422, detail="Invalid session ID format.")

    if limit < 1 or limit > MAX_LIMIT:
        raise HTTPException(
            status_code=400,
            detail=f"Limit must be between 1 and {MAX_LIMIT}",
        )

    if offset < 0:
        raise HTTPException(status_code=400, detail="Offset must be 0 or greater.")

    try:
        result = await db.execute(
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at)
            .limit(limit)
            .offset(offset)
        )

        messages = result.scalars().all()

        if not messages:
            logger.info(f"No messages found for session: {session_id}")
            return []

        logger.info(f"Retrieved {len(messages)} messages for session: {session_id}")
        return messages

    except Exception as e:
        logger.exception(f"Error fetching messages for session {session_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch messages")
