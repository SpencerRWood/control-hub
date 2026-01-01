import asyncio
import os

from backend.app.features.approvals.domain.models import ApprovalItem, ApprovalStatus
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

load_dotenv("/workspace/.env")

def _pick_db_url() -> str:
    """
    Explicit resolution order for scripts:
    1. DATABASE_URL (manual override)
    2. TEST_DATABASE_URL (default for seed/demo)
    """
    return os.getenv("DATABASE_URL")


async def main() -> None:
    db_url = _pick_db_url()
    if not db_url:
        raise RuntimeError(
            "No database URL found. Ensure /workspace/.env exists and contains "
            "TEST_DATABASE_URL (or set DATABASE_URL explicitly)."
        )

    engine = create_async_engine(db_url, future=True)
    SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

    async with SessionLocal() as session:
        session.add_all(
            [
                ApprovalItem(
                    title="Approve agent change",
                    description="Agent proposes config update",
                    type="AGENT_CONFIG",
                    payload_json={"k": "v"},
                    status=ApprovalStatus.PENDING,
                    requested_by="agent:foo",
                    assigned_to="user:spencer",
                ),
                # ApprovalItem(
                #     title="Deploy config v12",
                #     description="Ready to deploy",
                #     type="DEPLOY",
                #     payload_json={"env": "staging", "version": "12"},
                #     status=ApprovalStatus.APPROVED,
                #     requested_by="user:spencer",
                #     assigned_to="agent:deploy",
                #     decision_by="user:spencer",
                #     decision_reason="Looks good",
                # ),
            ]
        )
        await session.commit()

    await engine.dispose()


if __name__ == "__main__":
    print("ENV DATABASE_URL:", os.getenv("DATABASE_URL"))
    print("ENV TEST_DATABASE_URL:", os.getenv("TEST_DATABASE_URL"))
    asyncio.run(main())
