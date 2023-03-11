from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_DRIVER: str
    # DATABASE_URL: str = f'postgresql+asyncpg://postgres:postgres@db:5432/postgres'
    DATABASE_URL: PostgresDsn


settings = Settings()
