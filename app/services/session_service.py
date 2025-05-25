from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from uuid import UUID

from app.db.models import ChatSession
from app.schemas.session import ChatSessionCreate
from app.core.logging import logger


async def create_chat_session(
    db: AsyncSession, session_data: ChatSessionCreate
) -> ChatSession:
    try:
        if not session_data.user_id or not session_data.title:
            raise HTTPException(
                status_code=422, detail="User ID and title are required."
            )

        new_session = ChatSession(
            user_id=session_data.user_id, title=session_data.title
        )
        db.add(new_session)
        await db.commit()
        await db.refresh(new_session)
        logger.info(f"Created new session for user: {session_data.user_id}")
        return new_session

    except Exception as e:
        logger.exception(f"Failed to create chat session: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def get_chat_session_by_user(
    db: AsyncSession, user_id: str, is_favorite: bool = False
):
    try:
        if not user_id:
            raise HTTPException(status_code=422, detail="User ID is required.")

        query = select(ChatSession).where(ChatSession.user_id == user_id)
        if is_favorite:
            query = query.where(ChatSession.is_favorite == True)

        result = await db.execute(query.order_by(ChatSession.created_at.desc()))
        sessions = result.scalars().all()

        logger.info(
            f"Retrieved {len(sessions)} session(s) for user {user_id} (is_favorite={is_favorite})"
        )
        return sessions

    except Exception as e:
        logger.exception(f"Failed to fetch sessions for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def rename_chat_session(db: AsyncSession, session_id: str, new_title: str):
    try:
        if not new_title:
            raise HTTPException(status_code=422, detail="New title is required.")

        query = select(ChatSession).where(ChatSession.id == session_id)
        result = await db.execute(query)
        session = result.scalar_one_or_none()

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        session.title = new_title
        await db.commit()
        await db.refresh(session)

        logger.info(f"Renamed session {session_id} to '{new_title}'")
        return session

    except Exception as e:
        logger.exception(f"Failed to rename session {session_id}: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def set_favorite_status(db: AsyncSession, session_id: str, is_favorite: bool):
    try:
        query = select(ChatSession).where(ChatSession.id == session_id)
        result = await db.execute(query)
        session = result.scalar_one_or_none()

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        session.is_favorite = is_favorite
        await db.commit()
        await db.refresh(session)

        logger.info(f"Set favorite={is_favorite} for session {session_id}")
        return session

    except Exception as e:
        logger.exception(f"Failed to set favorite status for session {session_id}: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def delete_chat_session(db: AsyncSession, session_id: str):
    try:
        query = select(ChatSession).where(ChatSession.id == session_id)
        result = await db.execute(query)
        session = result.scalar_one_or_none()

        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        await db.delete(session)
        await db.commit()

        logger.info(f"Deleted session {session_id}")

    except Exception as e:
        logger.exception(f"Failed to delete session {session_id}: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
