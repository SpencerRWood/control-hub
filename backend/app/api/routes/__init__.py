# app/api/routes/__init__.py
from app.api.routes.approval_items import router as approvals_router
from app.api.routes.health import router as health_router
from app.api.routes.rag import router as rag_router
# from app.api.routes.agents import router as agents_router

all_routers = [
    (health_router, "/health", ["health"]),
    (approvals_router, "/approvals", ["approvals"]),
    (rag_router,"/rag",["rag"])
    # (agents_router, "/agents", ["agents"]),
]
