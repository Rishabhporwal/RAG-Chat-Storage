from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.schemas.message import ChatMessageCreate, ChatMessageOut
from app.services.message_service import add_messages, get_message_by_session

from app.db.session import get_db
from app.core.security import api_key_auth

router = APIRouter(prefix="/messages", tags=["Chat Messages"])


@router.post("/", response_model=ChatMessageOut, dependencies=[Depends(api_key_auth)])
async def create_message(
    message: ChatMessageCreate, db: AsyncSession = Depends(get_db)
):
    return await add_messages(db, message)


@router.get(
    "/session/{session_id}",
    response_model=List[ChatMessageOut],
    dependencies=[Depends(api_key_auth)],
)
async def get_messages(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
    limit: int = Query(20),
    offset: int = Query(0),
):
    return await get_message_by_session(db, session_id, limit, offset)
