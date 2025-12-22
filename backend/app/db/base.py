# app/db/base.py
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Import models so metadata is populated for Alembic
from app.models import approval_item  # noqa: F401
