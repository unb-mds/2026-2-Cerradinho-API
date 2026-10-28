import pytest

from app.core import cache
from app.core.rate_limit import limiter as rate_limiter


@pytest.fixture(autouse=True)
def cache_falso(monkeypatch):
    # evita que qualquer teste dependa de um redis real

    class _RedisFalso:
        def __init__(self):
            self.dados = {}

        def get(self, chave):
            return self.dados.get(chave)

        def set(self, chave, valor, ex=None):
            self.dados[chave] = valor

        def delete(self, *chaves):
            for c in chaves:
                self.dados.pop(c, None)

        def scan_iter(self, match):
            prefixo = match.rstrip("*")
            return [c for c in self.dados if c.startswith(prefixo)]

    monkeypatch.setattr(cache, "_cliente", _RedisFalso())

@pytest.fixture(autouse=True)
def rate_limit_desligado(monkeypatch):
    monkeypatch.setattr(rate_limiter, "enabled", False)