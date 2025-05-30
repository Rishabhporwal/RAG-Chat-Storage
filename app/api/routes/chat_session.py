from fastapi import APIRouter, Depends, Query, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.core.rate_limiter import limiter
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
from app.core.logging import logger

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
    try:
        logger.info(f"Creating chat session for user: {session.user_id}")
        return await create_chat_session(db, session)
    except Exception as e:
        logger.exception(f"Error creating session: {e}")
        raise HTTPException(status_code=500, detail="Failed to create chat session")


@router.get(
    "/", response_model=List[ChatSessionOut], dependencies=[Depends(api_key_auth)]
)
@limiter.limit("5/minute")
async def get_sessions(
    request: Request,
    user_id: str,
    is_favorite: Optional[bool] = Query(False),
    db: AsyncSession = Depends(get_db),
):
    try:
        logger.info(
            f"Fetching sessions for user: {user_id}, is_favorite: {is_favorite}"
        )
        return await get_chat_session_by_user(
            db, user_id=user_id, is_favorite=is_favorite
        )
    except Exception as e:
        logger.exception(f"Error fetching sessions for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch sessions")


@router.put(
    "/{session_id}/rename",
    response_model=ChatSessionOut,
    dependencies=[Depends(api_key_auth)],
)
async def rename_session(
    session_id: str, payload: RenameSession, db: AsyncSession = Depends(get_db)
):
    try:
        logger.info(f"Renaming session {session_id} to '{payload.title}'")
        return await rename_chat_session(
            db, session_id=session_id, new_title=payload.title
        )
    except Exception as e:
        logger.exception(f"Error renaming session {session_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to rename session")


@router.put(
    "/{session_id}/favorite",
    response_model=ChatSessionOut,
    dependencies=[Depends(api_key_auth)],
)
async def toggle_favorite(
    session_id: str, payload: FavoriteSession, db: AsyncSession = Depends(get_db)
):
    try:
        logger.info(f"Setting favorite={payload.is_favorite} for session {session_id}")
        return await set_favorite_status(
            db, session_id=session_id, is_favorite=payload.is_favorite
        )
    except Exception as e:
        logger.exception(f"Error setting favorite status for session {session_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to set favorite status")


@router.delete("/{session_id}", status_code=204, dependencies=[Depends(api_key_auth)])
async def delete_session(session_id: str, db: AsyncSession = Depends(get_db)):
    try:
        logger.info(f"Deleting session {session_id}")
        await delete_chat_session(db, session_id=session_id)
    except Exception as e:
        logger.exception(f"Error deleting session {session_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete session")
