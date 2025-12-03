from datetime import datetime

from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    api_key = Column(String, unique=True, index=True)  # The "Secret"
    is_active = Column(Boolean, default=True)


class LogEntry(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    level = Column(String, index=True)
    message = Column(String)
    meta_data = Column(JSON, nullable=True)  # Renamed to avoid reserved word conflict
    created_at = Column(DateTime, default=datetime.utcnow)
