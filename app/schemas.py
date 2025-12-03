# app/schemas.py
from datetime import datetime
from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, Field


class LogIngest(BaseModel):
    """Schema for the incoming log payload."""

    # Restrict levels to common logging levels for consistency
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        ..., description="The severity level of the log."
    )
    message: str = Field(..., description="The main content of the log message.")

    # Optional fields
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Arbitrary structured data related to the log."
    )
    timestamp: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="The time the log was generated (defaults to current UTC time if not provided).",
    )

    class Config:
        # Example to show expected format in documentation
        json_schema_extra = {
            "example": {
                "level": "INFO",
                "message": "User logged in successfully.",
                "metadata": {"user_id": 42, "ip_address": "192.168.1.1"},
            }
        }
