from typing import Any, Optional
from urllib.parse import urlparse

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_DRIVER: str
    DATABASE_URL: PostgresDsn = None

    class Config:
        """Конфиг класса."""

        env_file = ".env"
        env_file_encoding = "utf-8"

    @validator("DATABASE_URL", pre=True, allow_reuse=True)
    def assemble_db_connection(
        cls, v: Optional[str], values: dict[str, Any]
    ) -> str:
        """Собираем коннект для подключения к БД."""
        if isinstance(v, str):
            conn = urlparse(v)
            return PostgresDsn.build(
                scheme=conn.scheme,
                user=conn.username,
                password=conn.password,
                host=conn.hostname,
                port=str(conn.port),
                path=conn.path,
            )

        return PostgresDsn.build(
            scheme=values["DB_DRIVER"],
            user=values["DB_USER"],
            password=values["DB_PASS"],
            host=values["DB_HOST"],
            port=str(values["DB_PORT"]),
            path=f"/{values['DB_NAME']}",
        )


settings = Settings()
