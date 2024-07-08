""" User module
A Model of the user of the messaging service
belonging to an organisation in an application
"""
from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    """
    Implements User
    """
    org_id: str
    app_id: str
    full_name: str
    email: str
    password: str
    role: str
    created_at: int = int(datetime.timestamp(datetime.now()))
    updated_at: int = int(datetime.timestamp(datetime.now()))