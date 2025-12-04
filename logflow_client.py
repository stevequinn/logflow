import json
from datetime import datetime
from typing import Any, Dict, Literal, Optional

import httpx

# Define the acceptable log levels based on the LogFlow API schema
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class LogFlowClient:
    """
    A synchronous client for sending structured logs to the LogFlow API.
    """

    def __init__(self, api_url: str, api_key: str):
        """
        Initializes the LogFlow client.

        Args:
            api_url (str): The base URL of the LogFlow API (e.g., "http://localhost:8000").
            api_key (str): The project's secret API Key for authentication.
        """
        self.ingestion_url = f"{api_url.rstrip('/')}/logs"
        self.headers = {"Content-Type": "application/json", "X-API-Key": api_key}
        print(f"LogFlow client initialized for {self.ingestion_url}")

    def _send_log(
        self, level: LogLevel, message: str, metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[httpx.Response]:
        """
        Constructs the log payload and sends the POST request.
        """
        payload = [
            {
                "level": level.upper(),
                "message": message,
                "timestamp": datetime.utcnow().isoformat()
                + "Z",  # Use Z for UTC marker
                "metadata": metadata if metadata is not None else {},
            }
        ]

        try:
            # Use a synchronous client request
            response = httpx.post(
                self.ingestion_url, headers=self.headers, data=json.dumps(payload)
            )

            if response.status_code == 202:
                # Log successfully queued
                return response
            elif response.status_code == 401:
                print("LOGFLOW ERROR: Unauthorized (401). Check API Key.")
            else:
                print(
                    f"LOGFLOW ERROR: API returned status {response.status_code}. Response: {response.text}"
                )

        except httpx.RequestError as e:
            print(
                f"LOGFLOW CRITICAL: Failed to connect to API at {self.ingestion_url}. Error: {e}"
            )

        return None

    # --- Convenience Logging Methods ---

    def debug(self, message: str, metadata: Optional[Dict[str, Any]] = None):
        """Sends a DEBUG level log."""
        self._send_log("DEBUG", message, metadata)

    def info(self, message: str, metadata: Optional[Dict[str, Any]] = None):
        """Sends an INFO level log."""
        self._send_log("INFO", message, metadata)

    def warning(self, message: str, metadata: Optional[Dict[str, Any]] = None):
        """Sends a WARNING level log."""
        self._send_log("WARNING", message, metadata)

    def error(self, message: str, metadata: Optional[Dict[str, Any]] = None):
        """Sends an ERROR level log."""
        self._send_log("ERROR", message, metadata)

    def critical(self, message: str, metadata: Optional[Dict[str, Any]] = None):
        """Sends a CRITICAL level log."""
        self._send_log("CRITICAL", message, metadata)
