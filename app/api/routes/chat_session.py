from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.schemas.session import (
    ChatSessionCreate,
    ChatSessionOut,
    RenameSession,
    FavoriteSession,
)
from app.services.session_service import (
    create_chat_session,
    get_chat_session_by_user,
    rename_chat_session,
    set_favorite_status,
    delete_chat_session,
)
from app.db.session import get_db
from app.core.security import api_key_auth

router = APIRouter(prefix="/session", tags=["Chat Sessions"])


@router.post(
    "/",
    response_model=ChatSessionOut,
    status_code=201,
    dependencies=[Depends(api_key_auth)],
)
async def create_sessions(
    session: ChatSessionCreate, db: AsyncSession = Depends(get_db)
):
    return await create_chat_session(db, session)


@router.get(
    "/", response_model=List[ChatSessionOut], dependencies=[Depends(api_key_auth)]
)
async def get_sessions(
    user_id: str,
    is_favorite: Optional[bool] = Query(False),
    db: AsyncSession = Depends(get_db),
):
    return await get_chat_session_by_user(db, user_id=user_id, is_favorite=is_favorite)


@router.put(
    "/{session_id}/rename",
    response_model=ChatSessionOut,
    dependencies=[Depends(api_key_auth)],
)
async def rename_session(
    session_id: str, payload: RenameSession, db: AsyncSession = Depends(get_db)
):
    return await rename_chat_session(db, session_id=session_id, new_title=payload.title)


@router.put(
    "/{session_id}/favorite",
    response_model=ChatSessionOut,
    dependencies=[Depends(api_key_auth)],
)
async def toggle_favorite(
    session_id: str, payload: FavoriteSession, db: AsyncSession = Depends(get_db)
):
    return await set_favorite_status(
        db, session_id=session_id, is_favorite=payload.is_favorite
    )


@router.delete("/{session_id}", status_code=204, dependencies=[Depends(api_key_auth)])
async def delete_session(session_id: str, db: AsyncSession = Depends(get_db)):
    await delete_chat_session(db, session_id=session_id)
