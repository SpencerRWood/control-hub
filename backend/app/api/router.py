from app.core.health.router import router as health_router
from app.features.approvals.api.router import router as approvals_router
from app.features.rag.api.router import router as rag_router
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(approvals_router, prefix="/approvals", tags=["approvals"])
api_router.include_router(rag_router, prefix="/rag", tags=["rag"])