"""Normalização de texto pra busca parcial, sem acento nem caixa.

Compartilhado entre `app/domain/professores.py` e `app/domain/disciplinas.py`
(RF04, RF01) - os dois filtram em Python, não em SQL, porque acento/caixa
não são tratados de forma portável entre SQLite (testes) e Postgres
(produção) sem extensão (unaccent).
"""

import unicodedata


def normalizar_busca(texto: str) -> str:
    """ "andré" e "Andre" e "ANDRÉ" todos viram a mesma chave."""
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    return sem_acento.casefold()
