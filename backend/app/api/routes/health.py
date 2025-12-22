from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.session import get_session
from typing import Dict

router = APIRouter()

@router.get("/db_health")
def db_health(db: Session = Depends(get_session)) -> Dict[str,str]:
    db.execute(text("select 1"))
    return {"status": "ok"}

@router.get("/api_health") 
def health() -> Dict[str,str]:
    return {"status": "ok"}