from app.config import settings
from app.database import SessionLocal  # A synchronous session factory
from worker.backends import DatabaseBackend, FileBackend
from worker.celery_app import celery_app

# Initialize backends
file_backend = FileBackend()
db_backend = DatabaseBackend()


@celery_app.task(name="process_log")
def process_log(log_payload: dict):
    """
    Worker task.
    1. Always writes to File (for safety).
    2. Writes to DB if configured to do so.
    """
    # 1. Write to File
    if settings.ENABLE_FILE_LOGGING:
        file_backend.write(log_payload)

    # 2. Write to DB
    if settings.ENABLE_DB_LOGGING:
        # We open a new DB session for every task to ensure thread safety
        with SessionLocal() as db:
            db_backend.write(log_payload, db_session=db)

    return "Log processed"
