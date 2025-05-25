import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from datetime import datetime, timezone

from app.services import message_service
from app.db.models import ChatMessage
from app.schemas.message import ChatMessageCreate


@pytest.mark.asyncio
async def test_add_messages():
    db = AsyncMock()
    message_data = ChatMessageCreate(
        session_id=uuid4(), sender="user123", content="Hello there"
    )

    db.add = AsyncMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock(side_effect=lambda x: setattr(x, "id", uuid4()))

    result = await message_service.add_messages(db, message_data)

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()
    assert result.content == "Hello there"
    assert result.session_id == message_data.session_id
    assert result.sender == "user123"


@pytest.mark.asyncio
async def test_get_message_by_session():
    db = AsyncMock()
    session_id = uuid4()

    msg1 = ChatMessage(
        id=uuid4(),
        session_id=session_id,
        sender="user1",
        content="Hi",
        created_at=datetime.now(timezone.utc),
    )
    msg2 = ChatMessage(
        id=uuid4(),
        session_id=session_id,
        sender="assistant",
        content="Hello!",
        created_at=datetime.now(timezone.utc),
    )

    # Mocking the chain: db.execute().scalars().all()
    scalars_mock = MagicMock()
    scalars_mock.all.return_value = [msg1, msg2]

    execute_mock = MagicMock()
    execute_mock.scalars.return_value = scalars_mock

    db.execute.return_value = execute_mock

    result = await message_service.get_message_by_session(
        db, session_id=session_id, limit=10, offset=0
    )

    db.execute.assert_called_once()
    assert len(result) == 2
    assert result[0].content == "Hi"
    assert result[1].sender == "assistant"
