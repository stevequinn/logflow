# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Setup the synchronous engine for PostgreSQL
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# A session factory used to create new sessions
# autocommit=False: Ensures explicit transaction management
# autoflush=False: Prevents sessions from flushing automatically
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get a DB session (used by FastAPI)
def get_db_session():
    """Provides a transactional database session for FastAPI dependencies."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
