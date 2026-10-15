from datetime import datetime

from pydantic import BaseModel, Field


class Execucao(BaseModel):
    id: int = Field(description="Identificador interno do registro.", examples=[42])
    task_name: str = Field(
        description = "Nome completo da task do Celery.",
        examples = ["app.tasks.scraping.scrape_disciplinas_task"],
    )

    status: str = Field(description = "'sucesso' ou 'falha'.", examples = ["falha"])
    tipo_falha: str | None = Field(
        default = None,
        description = "Só preenchido em falha: 'fonte' (sites fora do ar) ou 'interna' (bug no código).",
        examples = ["fonte"],
    )

    mensagem: str | None = Field(default=None, description="Mensagem da exceção.",)

    criado_em: datetime = Field(description = "Quando a execução terminou.")