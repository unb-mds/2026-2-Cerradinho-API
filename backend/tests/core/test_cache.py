import json

from app.core import cache


class _RedisFalso:
    def __init__(self):
        self.dados = {}

    def get(self, chave):
        return self.dados.get(chave)

    def set(self, chave, valor, ex = None):
        self.dados[chave] = valor

    def delete(self, *chaves):
        for c in chaves:
            self.dados.pop(c, None)

    def scan_iter(self, match):
        prefixo = match.rstrip("*")
        return [c for c in self.dados if c.startswith(prefixo)]

def test_resposta_cacheada_grava_no_miss_e_ele_no_hit(monkeypatch):
    monkeypatch.setattr(cache, "_cliente", _RedisFalso())
    chamadas = {"n": 0}

    def calcular():
        chamadas["n"] += 1
        return [1, 2, 3]

    primeira = cache.resposta_cacheada("chave", 60, calcular, list[int])
    segunda = cache.resposta_cacheada("chave", 60, calcular, list[int])

    assert primeira == [1, 2, 3]
    assert json.loads(segunda.body) == [1, 2, 3]
    assert chamadas["n"] == 1

def test_invalidar_prefixo_apaga_so_as_chaves_do_prefixo(monkeypatch):
    falso = _RedisFalso()
    falso.dados = {"cache:v1:cardapio:semana:2026-10-20": "x", "cache:v1:disciplinas": "y"}
    monkeypatch.setattr(cache, "_cliente", falso)

    cache.invalidar_prefixo("cache:v1:cardapio:semana:")

    assert "cache:v1:cardapio:semana:2026-10-20" not in falso.dados
    assert "cache:v1:disciplinas" in falso.dados