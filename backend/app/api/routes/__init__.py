# app/api/routes/__init__.py
from app.api.routes.health import router as health_router
# from app.api.routes.approvals import router as approvals_router
# from app.api.routes.agents import router as agents_router

all_routers = [
    (health_router, "", ["health"]),
    # (approvals_router, "/approvals", ["approvals"]),
    # (agents_router, "/agents", ["agents"]),
]
