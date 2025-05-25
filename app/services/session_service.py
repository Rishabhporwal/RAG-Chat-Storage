from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from app.db.models import ChatSession
from app.schemas.session import ChatSessionCreate


async def create_chat_session(
    db: AsyncSession, session_data: ChatSessionCreate
) -> ChatSession:
    new_session = ChatSession(user_id=session_data.user_id, title=session_data.title)
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    return new_session


async def get_chat_session_by_user(
    db: AsyncSession, user_id: str, is_favorite: bool = False
):
    print("UserId", user_id)
    print("Is_Favorite", is_favorite)
    query = select(ChatSession).where(ChatSession.user_id == user_id)
    if is_favorite:
        query = query.where(ChatSession.is_favorite == True)
    result = await db.execute(query.order_by(ChatSession.created_at.desc()))
    return result.scalars().all()


async def rename_chat_session(db: AsyncSession, session_id: str, new_title: str):
    query = select(ChatSession).where(ChatSession.id == session_id)
    result = await db.execute(query)
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session.title = new_title
    await db.commit()
    await db.refresh(session)
    return session


async def set_favorite_status(db: AsyncSession, session_id: str, is_favorite: bool):
    query = select(ChatSession).where(ChatSession.id == session_id)
    result = await db.execute(query)
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session.is_favorite = is_favorite
    await db.commit()
    await db.refresh(session)
    return session


async def delete_chat_session(db: AsyncSession, session_id: str):
    query = select(ChatSession).where(ChatSession.id == session_id)
    result = await db.execute(query)
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    await db.delete(session)
    await db.commit()
