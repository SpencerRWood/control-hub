import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

CHAT_TABLES = {"chat_threads", "chat_messages"}


@pytest.mark.asyncio
async def test_chat_tables_exist(db_session: AsyncSession):
    # Postgres: query information_schema for tables in current schema
    res = await db_session.execute(
        text(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = current_schema()
            """
        )
    )
    existing = {row[0] for row in res.fetchall()}

    missing = CHAT_TABLES - existing
    assert not missing, f"Missing tables: {sorted(missing)}"
