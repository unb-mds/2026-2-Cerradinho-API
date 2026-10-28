import pytest

from app.core.config import Settings


@pytest.mark.parametrize(
    ("redis_url", "cache", "rate_limit"),
    [
        # padrão do docker compose, com o banco no path
        ("redis://redis:6379/0", "redis://redis:6379/2", "redis://redis:6379/3"),
        # formato do REDIS_URL do Railway, sem path: cortar no último "/"
        # dava "redis://2", que o Python resolve como o IP 0.0.0.2
        (
            "redis://default:senha@redis.railway.internal:6379",
            "redis://default:senha@redis.railway.internal:6379/2",
            "redis://default:senha@redis.railway.internal:6379/3",
        ),
    ],
)
def test_urls_do_cache_e_do_rate_limit_trocam_so_o_banco(redis_url, cache, rate_limit):
    settings = Settings(redis_url=redis_url)

    assert settings.redis_cache_url == cache
    assert settings.redis_rate_limit_url == rate_limit
