from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from uuid import UUID

from app.db.models import ChatSession
from app.schemas.session import ChatSessionCreate, ChatSessionUpdate


async def create_session(
    db: AsyncSession, session_data: ChatSessionCreate
) -> ChatSession:
    print("SessionData", session_data)
    new_session = ChatSession(**session_data.dict())
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    return new_session


async def get_session(db: AsyncSession, session_id: UUID) -> ChatSession:
    result = await db.execute(select(ChatSession).where(ChatSession.id == session_id))
    return result.scalar_one_or_none()


async def update_session(
    db: AsyncSession, session_id: UUID, updates: ChatSessionUpdate
) -> ChatSession:
    result = await db.execute(select(ChatSession).where(ChatSession.id == session_id))
    session = result.scalar_one_or_none()
    if session:
        for field, value in updates.dict(exclude_unset=True).items():
            setattr(session, field, value)

        await db.commit()
        await db.refresh(session)

    return session


async def delete_session(db: AsyncSession, session_id: UUID):
    result = db.execute(delete(ChatSession).where(ChatSession.id == session_id))
    await db.commit()
    return result


async def list_sessions(db: AsyncSession, user_id: str):
    result = await db.execute(
        select(ChatSession)
        .where(ChatSession.user_id == user_id)
        .order_by(ChatSession.created_at.desc())
    )

    return result.scalars().all()
