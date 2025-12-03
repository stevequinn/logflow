# worker/celery_app.py
from celery import Celery

from app.config import settings

# Initialize Celery app
celery_app = Celery("logflow_worker")

# Configure Celery using the settings object
celery_app.conf.update(
    broker_url=settings.CELERY_BROKER_URL,
    result_backend=settings.CELERY_RESULT_BACKEND,
    task_serializer=settings.CELERY_TASK_SERIALIZER,
    accept_content=settings.CELERY_ACCEPT_CONTENT,
    task_create_missing_queues=settings.CELERY_TASK_CREATE_MISSING_QUEUE,
    # Auto-discover tasks in the tasks.py module
    imports=("worker.tasks",),
    timezone="UTC",
)
