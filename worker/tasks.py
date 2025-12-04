from datetime import datetime

from app.config import settings
from app.database import SessionLocal  # A synchronous session factory
from worker.backends import DatabaseBackend, FileBackend
from worker.celery_app import celery_app

# Initialize backends
file_backend = FileBackend()
db_backend = DatabaseBackend()


@celery_app.task(name="process_log")
def process_log(log_payload: list[dict], id: int, name: str):
    """
    Worker task.
    1. Writes to File if configured to do so.
    2. Writes to DB if configured to do so.

    Future: Write to S3, Elasticsearch, etc.
    """

    for payload in log_payload:
        # Add some additional project related properties to each log entry
        payload["project_id"] = id
        payload["project_name"] = name
        if isinstance(payload["timestamp"], datetime):
            payload["timestamp"] = payload["timestamp"].isoformat()

    # 1. Write to File
    if settings.ENABLE_FILE_LOGGING:
        file_backend.write_many(log_payload)

    # 2. Write to DB
    if settings.ENABLE_DB_LOGGING:
        # We open a new DB session for every task to ensure thread safety
        with SessionLocal() as db:
            db_backend.write_many(log_payload, db_session=db)

    return f"{len(log_payload)} Logs processed"
