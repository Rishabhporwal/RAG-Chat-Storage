from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.schemas.session import ChatSessionCreate, ChatSessionOut, ChatSessionUpdate
from app.services.session_service import (
    create_session,
    get_session,
    update_session,
    delete_session,
    list_sessions,
)
from app.db.session import get_db
from app.core.security import api_key_auth

router = APIRouter(prefix="/session", tags=["Chat Sessions"])


@router.post("/", response_model=ChatSessionOut, dependencies=[Depends(api_key_auth)])
async def create_chat_session(
    session: ChatSessionCreate, db: AsyncSession = Depends(get_db)
):
    return await create_session(db, session)


@router.get(
    "/{session_id}", response_model=ChatSessionOut, dependencies=[Depends(api_key_auth)]
)
async def read_chat_session(session_id: UUID, db: AsyncSession = Depends(get_db)):
    session = await get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session Not Found")
    return session


@router.get(
    "/", response_model=List[ChatSessionOut], dependencies=[Depends(api_key_auth)]
)
async def list_chat_session(user_id: str, db: AsyncSession = Depends(get_db)):
    return await list_sessions(db, user_id)


@router.patch(
    "/{session_id}", response_model=ChatSessionOut, dependencies=[Depends(api_key_auth)]
)
async def update_chat_session(
    session_id: UUID, updates: ChatSessionUpdate, db: AsyncSession = Depends(get_db)
):
    session = await update_session(db, session_id, updates)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")


@router.delete("/{session_id}", status_code=204, dependencies=[Depends(api_key_auth)])
async def delete_chat_session(session_id: UUID, db: AsyncSession = Depends(get_db)):
    await delete_session(db, session_id)
