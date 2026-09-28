"""Contrato de dados para Disciplina/Turma/Professor/Sala (RF01-05).

Representa o formato validado que sai do scraper de Disciplinas antes de
seguir para o banco. Isso é intencionalmente "burro": normalização mais
profunda (ex: casar o mesmo professor com nomes grafados diferente entre
turmas, separar "FCTE - I9/I10" em prédio+sala) é responsabilidade da
camada de domínio (app/domain/), não deste contrato — evita duplicar essa
lógica entre o scraper e os endpoints, como o ARQUITETURA.md pede.
"""

from pydantic import BaseModel, Field


class Professor(BaseModel):
    nome: str = Field(description="Nome do docente como aparece no SIGAA.", examples=["Ana Souza"])


class Sala(BaseModel):
    # parsing em prédio/sala: ver app/domain/
    descricao: str = Field(
        description='Sala como o SIGAA publica, no formato "PRÉDIO - SALA". Vazio quando a turma não tem sala.',
        examples=["FCTE - I9/I10"],
    )


class Horario(BaseModel):
    codigo: str = Field(description="Código de horário do SIGAA: dia, turno e aulas.", examples=["6T2345"])
    descricao: str = Field(description="Horário por extenso.", examples=["Sexta-feira 14:00 às 17:50"])


class Turma(BaseModel):
    disciplina_codigo: str = Field(description="Código da disciplina.", examples=["FGA0242"])
    disciplina_nome: str = Field(
        description="Nome da disciplina.", examples=["Métodos de Desenvolvimento de Software"]
    )
    numero: str = Field(description="Número da turma dentro da disciplina.", examples=["01"])
    ano_periodo: str = Field(description="Ano e período letivo.", examples=["2026.2"])
    professores: list[Professor] = Field(description="Docentes da turma.")
    horarios: list[Horario] = Field(description="Horários de aula da turma.")
    sala: Sala = Field(description="Sala onde a turma tem aula.")
    vagas_ofertadas: int = Field(description="Total de vagas da turma.", examples=[40])
    vagas_ocupadas: int = Field(description="Vagas já preenchidas.", examples=[38])
