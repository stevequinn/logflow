import json
import os
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from models.orm import LogEntry


class LogBackend:
    def write(self, data: dict, db_session: Optional[Session] = None) -> None:
        raise NotImplementedError


class FileBackend(LogBackend):
    def __init__(self, base_path="logs_storage"):
        self.base_path = base_path

    def write(self, data: dict, db_session: Optional[Session] = None) -> None:
        """
        Writes logs to: logs_storage/{project_name}/{YYYY-MM-DD}.jsonl
        This acts as daily rotation.
        """
        project_name = data.get("project_name", "unknown")
        # Ensure safe filename
        safe_project_name = "".join(
            [c for c in project_name if c.isalnum() or c in ("-", "_")]
        ).strip()

        # Create folder: logs_storage/project-alpha/
        directory = os.path.join(self.base_path, safe_project_name)
        os.makedirs(directory, exist_ok=True)

        # File: 2023-10-27.jsonl
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        filepath = os.path.join(directory, f"{date_str}.jsonl")

        # Write mode 'a' (append) is atomic on POSIX systems for short writes
        try:
            with open(filepath, "a", encoding="utf-8") as f:
                f.write(json.dumps(data) + "\n")
        except Exception as e:
            # Fallback print if disk is full or permissions fail
            print(f"CRITICAL: Could not write to file backend: {e}")


class DatabaseBackend(LogBackend):
    def write(self, data: dict, db_session: Optional[Session] = None) -> None:
        if not db_session:
            raise ValueError("Database session required for DB backend")

        log_entry = LogEntry(
            project_id=data["project_id"],
            level=data["level"],
            message=data["message"],
            meta_data=data.get("metadata"),
            created_at=datetime.fromisoformat(data["timestamp"]),
        )
        db_session.add(log_entry)
        db_session.commit()
