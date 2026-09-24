from fastapi import FastAPI

from app.routers import cardapio, disciplinas

app = FastAPI(title="Cerradinho API", version="0.1.0")

app.include_router(disciplinas.router, prefix="/v1")
app.include_router(cardapio.router, prefix="/v1")
