import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/zoneer")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "CHANGE_ME")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    # OAuth providers (set in .env for real integrations)
    GOOGLE_CLIENT_ID: str | None = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str | None = os.getenv("GOOGLE_CLIENT_SECRET")
    MICROSOFT_CLIENT_ID: str | None = os.getenv("MICROSOFT_CLIENT_ID")
    MICROSOFT_CLIENT_SECRET: str | None = os.getenv("MICROSOFT_CLIENT_SECRET")
    FRONTEND_URL: str | None = os.getenv("FRONTEND_URL")

    # SMTP / Email (optional)
    SMTP_HOST: str | None = os.getenv("SMTP_HOST")
    SMTP_PORT: int | None = int(os.getenv("SMTP_PORT")) if os.getenv("SMTP_PORT") else None
    SMTP_USERNAME: str | None = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD: str | None = os.getenv("SMTP_PASSWORD")
    SMTP_FROM: str | None = os.getenv("SMTP_FROM")
settings = Settings()
