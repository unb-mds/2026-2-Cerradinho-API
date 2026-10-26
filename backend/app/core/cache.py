import logging

import redis
from fastapi import Response
from pydantic import TypeAdapter

from app.core.config import settings

logger = logging.getLogger(__name__)

TTL_SEMANAL = 60 * 60 * 24 * 7  # disciplinas/professores/salas
TTL_DIARIO = 60 * 60 * 24  # cardápio

_cliente = redis.Redis.from_url(settings.redis_cache_url, decode_responses=True)


def _buscar(chave: str) -> str | None:
    try:
        return _cliente.get(chave)
    except redis.RedisError:
        logger.warning("Falha ao ler cache (chave=%s), seguindo sem cache", chave)
        return None


def _gravar(chave: str, valor: str, ttl_segundos: int) -> None:
    try:
        _cliente.set(chave, valor, ex=ttl_segundos)
    except redis.RedisError:
        logger.warning("Falha ao gravar cache (chave=%s), seguindo sem cache", chave)


def invalidar(chave: str) -> None:
    try:
        _cliente.delete(chave)
    except redis.RedisError:
        logger.warning("Falha ao invalidar cache (chave=%s)", chave)


def invalidar_prefixo(prefixo: str) -> None:
    try:
        chaves = list(_cliente.scan_iter(match=f"{prefixo}*"))
        if chaves:
            _cliente.delete(*chaves)
    except redis.RedisError:
        logger.warning("Falha ao invalidar cache (prefixo=%s)", prefixo)


def resposta_cacheada(chave: str, ttl: int, calcular, tipo):
    hit = _buscar(chave)
    if hit is not None:
        return Response(content=hit, media_type="application/json")

    resultado = calcular()
    corpo = TypeAdapter(tipo).dump_json(resultado).decode("utf-8")
    _gravar(chave, corpo, ttl)
    return resultado