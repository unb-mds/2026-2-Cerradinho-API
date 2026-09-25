from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import cardapio, disciplinas

app = FastAPI(title="Cerradinho API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(disciplinas.router, prefix="/v1")
app.include_router(cardapio.router, prefix="/v1")
