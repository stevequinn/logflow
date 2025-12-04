import json
import os
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from models.orm import LogEntry


class LogBackend:
    def write(self, data: dict, db_session: Optional[Session] = None) -> None:
        raise NotImplementedError

    def write_many(
        self, data: list[dict], db_session: Optional[Session] = None
    ) -> None:
        raise NotImplementedError


class FileBackend(LogBackend):
    def __init__(self, base_path="logs_storage"):
        self.base_path = base_path

    def _get_filepath(self, project_name: str) -> str:
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

        return filepath

    def write(self, data: dict, db_session: Optional[Session] = None) -> None:
        """
        Writes logs to: logs_storage/{project_name}/{YYYY-MM-DD}.jsonl
        This acts as daily rotation.
        """
        project_name = data.get("project_name", "unknown")
        filepath = self._get_filepath(project_name)

        # Write mode 'a' (append) is atomic on POSIX systems for short writes
        try:
            with open(filepath, "a", encoding="utf-8") as f:
                f.write(json.dumps(data) + "\n")
        except Exception as e:
            # Fallback print if disk is full or permissions fail
            print(f"CRITICAL: Could not write to file backend: {e}")

    def write_many(
        self, data: list[dict], db_session: Optional[Session] = None
    ) -> None:
        """
        Writes logs to: logs_storage/{project_name}/{YYYY-MM-DD}.jsonl
        This acts as daily rotation.
        """
        project_name = data[0].get("project_name", "unknown")
        filepath = self._get_filepath(project_name)

        # Write mode 'a' (append) is atomic on POSIX systems for short writes
        try:
            with open(filepath, "a", encoding="utf-8") as f:
                f.writelines([json.dumps(log) + "\n" for log in data])
        except Exception as e:
            # Fallback print if disk is full or permissions fail
            print(f"CRITICAL: Could not write many to file backend: {e}")


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

    def write_many(
        self, data: list[dict], db_session: Optional[Session] = None
    ) -> None:
        if not db_session:
            raise ValueError("Database session required for DB backend")

        objects = [
            LogEntry(
                project_id=log["project_id"],
                level=log["level"],
                message=log["message"],
                meta_data=log.get("metadata"),
                created_at=datetime.fromisoformat(log["timestamp"]),
            )
            for log in data
        ]

        db_session.add_all(objects)
        db_session.commit()
