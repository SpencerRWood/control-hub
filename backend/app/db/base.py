# app/db/base.py
from app.models import approval_item  # noqa: E402, F401
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


