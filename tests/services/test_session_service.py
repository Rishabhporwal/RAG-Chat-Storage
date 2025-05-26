import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from uuid import uuid4

from app.services import session_service
from app.db.models import ChatSession
from app.schemas.session import ChatSessionCreate


@pytest.mark.asyncio
async def test_create_chat_session():
    db = AsyncMock()
    session_data = ChatSessionCreate(user_id="user123", title="Session 1")

    db.add = AsyncMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()

    db.refresh.side_effect = lambda x: setattr(x, "id", "1")

    result = await session_service.create_chat_session(db, session_data)

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()
    assert result.user_id == "user123"
    assert result.title == "Session 1"


@pytest.mark.asyncio
async def test_get_chat_session_by_user_all():
    db = AsyncMock()
    session1 = ChatSession(id="1", user_id="user123", title="s1")
    session2 = ChatSession(id="2", user_id="user123", title="s2")

    scalars_mock = MagicMock()
    scalars_mock.all.return_value = [session1, session2]

    execute_result = MagicMock()
    execute_result.scalars.return_value = scalars_mock
    db.execute.return_value = execute_result

    result = await session_service.get_chat_session_by_user(db, user_id="user123")

    db.execute.assert_called_once()
    assert len(result) == 2
    assert result[0].title == "s1"
    assert result[1].title == "s2"


@pytest.mark.asyncio
async def test_rename_chat_session_success():
    db = AsyncMock()
    session = ChatSession(id="123", title="Old Title")
    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = session
    db.execute.return_value = result_mock

    db.commit = AsyncMock()
    db.refresh = AsyncMock()

    result = await session_service.rename_chat_session(
        db, session_id="123", new_title="New Title"
    )

    assert result.title == "New Title"
    db.commit.assert_called_once()
    db.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_rename_chat_session_not_found():
    db = AsyncMock()
    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = None
    db.execute.return_value = result_mock

    with pytest.raises(HTTPException) as e:
        await session_service.rename_chat_session(
            db, session_id="123", new_title="New Title"
        )

    assert e.value.status_code == 500
    assert e.value.detail == "Internal Server Error"


@pytest.mark.asyncio
async def test_set_favorite_status_success():
    db = AsyncMock()
    session = ChatSession(id="123", title="Session", is_favorite=False)
    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = session
    db.execute.return_value = result_mock

    db.commit = AsyncMock()
    db.refresh = AsyncMock()

    result = await session_service.set_favorite_status(
        db, session_id="123", is_favorite=True
    )

    assert result.is_favorite is True
    db.commit.assert_called_once()
    db.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_set_favorite_status_not_found():
    db = AsyncMock()
    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = None
    db.execute.return_value = result_mock

    with pytest.raises(HTTPException) as e:
        await session_service.set_favorite_status(
            db, session_id="123", is_favorite=True
        )

    assert e.value.status_code == 500
    assert e.value.detail == "Internal Server Error"


@pytest.mark.asyncio
async def test_delete_chat_session_success():
    db = AsyncMock()
    session = ChatSession(id="123", title="Session")
    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = session
    db.execute.return_value = result_mock

    db.delete = AsyncMock()
    db.commit = AsyncMock()

    await session_service.delete_chat_session(db, session_id="123")

    db.delete.assert_called_once_with(session)
    db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_delete_chat_session_not_found():
    db = AsyncMock()
    result_mock = MagicMock()
    result_mock.scalar_one_or_none.return_value = None
    db.execute.return_value = result_mock

    session_id = uuid4()

    with pytest.raises(HTTPException) as e:
        await session_service.delete_chat_session(db, session_id=session_id)

    assert e.value.status_code == 500
    assert e.value.detail == "Internal Server Error"
