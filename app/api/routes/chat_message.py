from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.schemas.message import ChatMessageCreate, ChatMessageOut
from app.services.message_service import add_messages, get_message_by_session
from app.db.session import get_db
from app.core.security import api_key_auth
from app.core.logging import logger

router = APIRouter(prefix="/messages", tags=["Chat Messages"])


@router.post("/", response_model=ChatMessageOut, dependencies=[Depends(api_key_auth)])
async def create_message(
    message: ChatMessageCreate, db: AsyncSession = Depends(get_db)
):
    try:
        logger.info(f"Creating message for session: {message.session_id}")
        return await add_messages(db, message)
    except Exception as e:
        logger.exception(
            f"Error creating message for session {message.session_id}: {e}"
        )
        raise HTTPException(status_code=500, detail="Failed to create message")


@router.get(
    "/session/{session_id}",
    response_model=List[ChatMessageOut],
    dependencies=[Depends(api_key_auth)],
)
async def get_messages(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    try:
        logger.info(
            f"Fetching messages for session {session_id} | limit={limit}, offset={offset}"
        )
        return await get_message_by_session(db, session_id, limit, offset)
    except Exception as e:
        logger.exception(f"Error fetching messages for session {session_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch messages")
