from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIASGIMiddleware

from app.core.config import settings
from app.core.rate_limit import limiter
from app.routers import cardapio, disciplinas, execucoes, professores, salas

DESCRICAO = """
API pública que reúne dados institucionais da UnB hoje espalhados em vários sistemas:
disciplinas, professores, salas e cardápio do RU.

Os dados vêm só de fontes públicas (SIGAA público e site do RU) e são coletados
automaticamente por scrapers agendados. A API apenas lê o que já foi coletado, então
as respostas não dependem de a fonte estar no ar na hora da requisição.

Todas as rotas ficam sob `/v1/`. Mudanças incompatíveis no formato das respostas vão
para uma nova versão, sem quebrar quem já usa esta.

Código e documentação: https://github.com/unb-mds/2026-2-Cerradinho-API
"""

TAGS = [
    {"name": "disciplinas", "description": "Turmas ofertadas no período, com horário, sala, professores e vagas."},
    {"name": "cardapio", "description": "Cardápio do Restaurante Universitário (campus Darcy Ribeiro)."},
    {"name": "professores", "description": "Docentes que dão aula no período e as disciplinas de cada um."},
    {"name": "salas", "description": "Salas e prédios onde há aula, derivados das turmas do SIGAA."},
]

app = FastAPI(title="Cerradinho API", version="1.0.0", description=DESCRICAO, openapi_tags=TAGS)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIASGIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(disciplinas.router, prefix="/v1")
app.include_router(cardapio.router, prefix="/v1")
app.include_router(professores.router, prefix="/v1")
app.include_router(salas.router, prefix="/v1")
app.include_router(execucoes.router, prefix="/v1")
