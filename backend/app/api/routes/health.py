from typing import Dict

from app.db.session_sync import get_session
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/db")
def db_health(db: Session = Depends(get_session)) -> Dict[str,str]:
    db.execute(text("select 1"))
    return {"status": "ok"}

@router.get("/api") 
def health() -> Dict[str,str]:
    return {"status": "ok"}