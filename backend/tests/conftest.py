import pytest
from app.core.config import settings
from app.db.base import Base
from app.db.session_async import get_session
from app.main import app
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


@pytest.fixture(scope="module")
def test_database_url() -> str:
    return settings.test_database_url or settings.database_url


@pytest.fixture(scope="module")
async def engine(test_database_url: str):
    engine_ = create_async_engine(test_database_url, future=True)
    try:
        yield engine_
    finally:
        await engine_.dispose()


@pytest.fixture(scope="module")
def sessionmaker(engine):
    return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@pytest.fixture
def override_get_session(sessionmaker):
    async def _override():
        async with sessionmaker() as session:
            yield session

    return _override


@pytest.fixture(autouse=True)
async def _db_schema_per_test(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def async_client(override_get_session):
    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
