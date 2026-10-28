from urllib.parse import urlsplit, urlunsplit

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    postgres_user: str = "cerradinho"
    postgres_password: str = "cerradinho"
    postgres_db: str = "cerradinho"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    # Broker e backend de resultados do Celery. O padrão usa o nome do serviço
    # no docker compose; em produção o Railway passa o REDIS_URL do serviço Redis.
    redis_url: str = "redis://redis:6379/0"

    # Origens que o navegador pode usar pra chamar a API (o front Next.js roda em outra porta)
    cors_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def redis_cache_url(self) -> str:
        return _trocar_banco_redis(self.redis_url, 2)

    @property
    def redis_rate_limit_url(self) -> str:
        return _trocar_banco_redis(self.redis_url, 3)


def _trocar_banco_redis(url: str, banco: int) -> str:
    """Troca o número do banco no path da URL. O REDIS_URL do Railway vem
    sem path ("redis://default:senha@host:6379"), então não dá pra cortar
    no último "/", que nesse caso é o de "redis://"."""
    return urlunsplit(urlsplit(url)._replace(path=f"/{banco}"))


settings = Settings()
