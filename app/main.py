# app/main.py
from typing import List

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
    log_data: List[LogIngest],
    # The get_project dependency authenticates the request via X-API-Key
    project: Project = Depends(get_project),
):
    """
    Accepts a structured log payload list, validates the API key,
    and queues it for asynchronous processing by Celery.
    """
    # print(f"Received {len(log_data)} logs for project: {project.name}")

    payload = [log.model_dump() for log in log_data]
    task = process_log.delay(payload, project.id, project.name)  # pyright: ignore[reportFunctionMemberAccess]

    # Return 202 Accepted status
    return {
        "status": "queued",
        "task_id": task.id,
        "count": len(payload),
    }


# Optional: Root endpoint for health check
@app.get("/", include_in_schema=False, status_code=200)
async def root():
    return {"service": "LogFlow", "status": "running"}
