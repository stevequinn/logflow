# app/config.py
import os
from typing import Literal

# Ensure dotfiles are loaded for local testing
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # --- Infrastructure Settings ---
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://user:password@localhost:5432/logflow_db"
    )
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # --- Celery Configuration ---
    CELERY_BROKER_URL: str = REDIS_URL
    CELERY_RESULT_BACKEND: str = REDIS_URL
    CELERY_TASK_SERIALIZER: Literal["json"] = "json"
    CELERY_ACCEPT_CONTENT: tuple = ("json",)
    CELERY_TASK_CREATE_MISSING_QUEUE: bool = True

    # --- Logging Backend Flags (Used by Celery Worker) ---
    # Set these in your docker-compose or .env file
    ENABLE_DB_LOGGING: bool = True
    ENABLE_FILE_LOGGING: bool = True
    LOG_STORAGE_PATH: str = "logs_storage"


settings = Settings()
