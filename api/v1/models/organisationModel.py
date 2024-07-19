"""
Organisation model
"""
from pydantic import BaseModel
from datetime import datetime


class Organisation(BaseModel):
    """
    Implements Organisation
    """
    name: str
    owner: str
    apps: list
    created_at: int = int(datetime.timestamp(datetime.now()))
    updated_at: int = int(datetime.timestamp(datetime.now()))