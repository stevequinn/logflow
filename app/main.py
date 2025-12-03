# app/main.py
from datetime import datetime

from fastapi import Depends, FastAPI

# Local imports
from app.dependencies import get_project
from app.schemas import LogIngest
from models.orm import Project
from worker.tasks import process_log  # The task defined in worker/tasks.py

# Initialize FastAPI application
app = FastAPI(
    title="LogFlow Ingestion API",
    description="High-throughput asynchronous logging service.",
)


@app.post("/logs", status_code=202, summary="Ingest a Log Entry")
async def ingest_log(
    log_data: LogIngest,
    # The get_project dependency authenticates the request via X-API-Key
    project: Project = Depends(get_project),
):
    """
    Accepts a structured log payload, validates the API key, enriches the data,
    and queues it for asynchronous processing by Celery.
    """

    # Convert Pydantic model to dict
    payload = log_data.model_dump()

    # Enrich payload with project info and ensure timestamp is ISO format for safe transport
    payload["project_id"] = project.id
    payload["project_name"] = project.name

    # Ensure timestamp is ISO string format
    if isinstance(payload["timestamp"], datetime):
        payload["timestamp"] = payload["timestamp"].isoformat()

    # Push to Celery using .delay() (fire-and-forget)
    process_log.delay(payload)  # pyright: ignore[reportFunctionMemberAccess]

    # Return 202 Accepted status
    return {"status": "queued", "message": f"Log from {project.name} accepted."}


# Optional: Root endpoint for health check
@app.get("/", include_in_schema=False, status_code=200)
async def root():
    return {"service": "LogFlow", "status": "running"}
