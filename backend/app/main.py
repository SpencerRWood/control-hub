# app/main.py
from app.api.routes import all_routers
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Control Hub API")

for router, prefix, tags in all_routers:
    app.include_router(router, prefix=prefix, tags=tags)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
