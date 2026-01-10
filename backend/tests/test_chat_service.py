# backend/tests/features/chat/test_chat_service.py
import pytest

from app.features.chat.domain.enums import ChatRole
from app.features.chat.domain.schemas import ChatMessageCreate, ChatThreadCreate
from app.features.chat.repo import messages as message_repo
from app.features.chat.services.chat_service import ChatService


@pytest.mark.asyncio
async def test_chat_create_thread_persists_thread(db_session):
    svc = ChatService(session=db_session)

    thread = await svc.create_thread(
        ChatThreadCreate(
            title="Test Thread",
            created_by="user:spencer",
            metadata_json={"source": "pytest"},
        )
    )

    assert thread.thread_id
    assert thread.title == "Test Thread"
    assert thread.created_by == "user:spencer"
    assert thread.metadata_json["source"] == "pytest"


@pytest.mark.asyncio
async def test_chat_post_message_creates_user_and_assistant_messages(db_session):
    svc = ChatService(session=db_session)

    thread = await svc.create_thread(
        ChatThreadCreate(title=None, created_by="user:spencer", metadata_json={})
    )

    resp = await svc.post_message(
        thread_id=thread.thread_id,
        body=ChatMessageCreate(
            content="Hello",
            use_rag=False,
            max_citations=0,
            metadata_json={"client": "unit-test"},
        ),
    )

    assert resp.user_message.thread_id == thread.thread_id
    assert resp.user_message.role == ChatRole.USER
    assert resp.user_message.content == "Hello"
    assert resp.user_message.metadata_json["client"] == "unit-test"

    assert resp.assistant_message.thread_id == thread.thread_id
    assert resp.assistant_message.role == ChatRole.ASSISTANT
    assert resp.assistant_message.content  # stubbed content exists
    assert resp.assistant_message.metadata_json.get("stubbed") is True


@pytest.mark.asyncio
async def test_chat_get_thread_detail_returns_messages_in_order(db_session):
    svc = ChatService(session=db_session)

    thread = await svc.create_thread(
        ChatThreadCreate(title="Ordering", created_by="user:spencer", metadata_json={})
    )

    # Two turns
    await svc.post_message(thread_id=thread.thread_id, body=ChatMessageCreate(content="m1", metadata_json={}))
    await svc.post_message(thread_id=thread.thread_id, body=ChatMessageCreate(content="m2", metadata_json={}))

    detail = await svc.get_thread_detail(thread_id=thread.thread_id, limit=200, offset=0)

    assert detail.thread.thread_id == thread.thread_id
    assert len(detail.messages) == 4  # 2 user + 2 assistant

    roles = [m.role for m in detail.messages]
    assert roles == [ChatRole.USER, ChatRole.ASSISTANT, ChatRole.USER, ChatRole.ASSISTANT]

    contents = [m.content for m in detail.messages]
    assert contents[0] == "m1"
    assert contents[2] == "m2"


@pytest.mark.asyncio
async def test_chat_repo_list_by_thread_id_matches_service(db_session):
    svc = ChatService(session=db_session)

    thread = await svc.create_thread(
        ChatThreadCreate(title="Repo", created_by="user:spencer", metadata_json={})
    )
    await svc.post_message(thread_id=thread.thread_id, body=ChatMessageCreate(content="hello", metadata_json={}))

    rows = await message_repo.list_by_thread_id(db_session, thread_id=thread.thread_id, limit=50, offset=0)
    assert len(rows) == 2
    assert rows[0].role == ChatRole.USER.value
    assert rows[1].role == ChatRole.ASSISTANT.value
