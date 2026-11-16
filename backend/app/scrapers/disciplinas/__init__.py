"""Ponto de entrada público do scraper de Disciplinas (RF01-05).

Orquestra scraper.py (captura via Playwright) + parser.py (validação via
BeautifulSoup + Pydantic), expondo só o resultado já validado. Quem chama
isso daqui (uma task do Celery, por exemplo) não precisa saber que por
baixo tem Playwright/BeautifulSoup — só recebe list[Turma].
"""

from app.core.exceptions import ErroFonteIndisponivel
from app.schemas.disciplina import Turma

from .parser import listar_unidades, parse_turmas
from .scraper import DisciplinaScraper

__all__ = ["DisciplinaScraper", "raspar_disciplinas", "raspar_disciplinas_varias_unidades"]


async def raspar_disciplinas(nivel: str, unidade: str, ano: str, periodo: str) -> list[Turma]:
    """Captura e valida as turmas de uma unidade. Este é o contrato
    público do módulo: entrada = filtros de busca, saída = list[Turma]."""
    scraper = DisciplinaScraper()
    html = await scraper.buscar_html(nivel, unidade, ano, periodo)
    return parse_turmas(html)


async def raspar_disciplinas_varias_unidades(
    nivel: str,
    ano: str,
    periodo: str,
    unidades: list[str] | None = None,
) -> dict[str, list[Turma]]:
    """Mesma coisa, para várias unidades de uma vez. Se `unidades` for
    None, varre todas as unidades listadas no formulário do SIGAA.

    Devolve {codigo_unidade: turmas} em vez de uma lista só — Turma.unidade
    é obrigatório no banco (app/models/turma.py), e o código da unidade não
    vem em nenhum campo do HTML da própria turma, só na página de busca. Uma
    lista achatada perderia essa informação sem volta.

    Falha alto em vez de devolver um dict vazio, que a task registraria
    como sucesso com zero turmas (RNF05):
    - ErroFonteIndisponivel se nenhuma unidade respondeu (SIGAA fora do ar
      ou sessão expirada em todas);
    - ValueError se o formulário não tem a lista de unidades ou se nenhuma
      unidade tem turma, os dois sinais de que o layout mudou."""
    scraper = DisciplinaScraper()

    if unidades is None:
        html_formulario = await scraper.obter_html_formulario()
        unidades = [codigo for codigo, _ in listar_unidades(html_formulario)]
        if not unidades:
            raise ValueError("Formulário de busca do SIGAA sem a lista de unidades: o layout pode ter mudado.")

    html_por_unidade = await scraper.buscar_html_varias_unidades(nivel, ano, periodo, unidades)
    if unidades and not html_por_unidade:
        raise ErroFonteIndisponivel(f"Nenhuma das {len(unidades)} unidade(s) respondeu à busca no SIGAA.")

    turmas_por_unidade = {
        codigo_unidade: parse_turmas(html)
        for codigo_unidade, html in html_por_unidade.items()
    }
    if turmas_por_unidade and not any(turmas_por_unidade.values()):
        raise ValueError(
            f"Nenhuma turma encontrada nas {len(turmas_por_unidade)} unidade(s) que responderam: "
            "o layout do resultado pode ter mudado."
        )
    return turmas_por_unidade
