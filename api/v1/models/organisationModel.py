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
    apps: list
    token: str
    created_at: int = int(datetime.timestamp(datetime.now()))
    updated_at: int = int(datetime.timestamp(datetime.now()))