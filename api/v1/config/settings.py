"""
settings module

Centralised application configuration loaded from environment variables.
Copy .env.example to .env and fill in your values before running.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    DB_NAME: str = os.getenv("DB_NAME", "nkhunda_messaging_api_db")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))


settings = Settings()

if not settings.SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY environment variable is not set. "
        "Copy .env.example to .env and set a strong secret key."
    )
