import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.db.base import Base
from app.db.session_async import get_session
from app.main import app


@pytest.fixture
def test_database_url() -> str:
    return settings.test_database_url or settings.database_url


# Function-scoped engine avoids "Future attached to a different loop" teardown errors
@pytest_asyncio.fixture
async def engine(test_database_url: str):
    engine_ = create_async_engine(test_database_url, future=True)
    try:
        yield engine_
    finally:
        await engine_.dispose()


@pytest.fixture
def sessionmaker(engine):
    return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@pytest_asyncio.fixture
async def db_session(sessionmaker):
    async with sessionmaker() as session:
        yield session


@pytest.fixture
def override_get_session(sessionmaker):
    async def _override():
        async with sessionmaker() as session:
            yield session
    return _override


@pytest_asyncio.fixture(autouse=True)
async def _db_schema_per_test(engine):
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def async_client(override_get_session):
    app.dependency_overrides[get_session] = override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()
