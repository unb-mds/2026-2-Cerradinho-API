from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import cardapio, disciplinas, professores, salas

DESCRICAO = """
API pública que reúne dados institucionais da UnB hoje espalhados em vários sistemas:
disciplinas, professores, salas e cardápio do RU.

Os dados vêm só de fontes públicas (SIGAA público e site do RU) e são coletados
automaticamente por scrapers agendados. A API apenas lê o que já foi coletado, então
as respostas não dependem de a fonte estar no ar na hora da requisição.

Todas as rotas ficam sob `/v1/`. Mudanças incompatíveis no formato das respostas vão
para uma nova versão, sem quebrar quem já usa esta.

Código e documentação: https://github.com/unb-mds/G3-2026-2
"""

TAGS = [
    {"name": "disciplinas", "description": "Turmas ofertadas no período, com horário, sala, professores e vagas."},
    {"name": "cardapio", "description": "Cardápio do Restaurante Universitário (campus Darcy Ribeiro)."},
    {"name": "professores", "description": "Docentes que dão aula no período e as disciplinas de cada um."},
    {"name": "salas", "description": "Salas e prédios onde há aula, derivados das turmas do SIGAA."},
]

app = FastAPI(title="Cerradinho API", version="1.0.0", description=DESCRICAO, openapi_tags=TAGS)

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
