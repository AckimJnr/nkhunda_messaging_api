""" User module
A Model of the user of the messaging service
belonging to an organisation in an application
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class User(BaseModel):
    """
    Implements User
    """
    full_name: str
    email: str
    hashed_password: str
    role: str
    created_at: int = int(datetime.timestamp(datetime.now()))
    updated_at: int = int(datetime.timestamp(datetime.now()))