from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    postgres_user: str = "cerradinho"
    postgres_password: str = "cerradinho"
    postgres_db: str = "cerradinho"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    # Origens que o navegador pode usar pra chamar a API (o front Next.js roda em outra porta)
    cors_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
