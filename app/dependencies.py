from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from models.orm import Project

from .database import get_db_session


async def get_project(
    x_api_key: str = Header(...), db: Session = Depends(get_db_session)
):
    """
    Validates the API Key and returns the Project object.
    If invalid, raises 401.
    """
    pro = db.query(Project).filter(Project.api_key == x_api_key).first()

    if not pro or not pro.is_active:
        raise HTTPException(status_code=401, detail="Invalid or inactive API Key")

    return pro
