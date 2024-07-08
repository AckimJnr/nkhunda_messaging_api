""" Message module
A Model of the message of the messaging service
"""
from pydantic import BaseModel
from datetime import datetime


class Message(BaseModel):
    """
    Implements a message
    """
    app_id: str
    message_type: str
    group_id: str
    status: str
    message_content: str
    sender_id: str
    recipient_id: str
    created_at: int = int(datetime.timestamp(datetime.now()))
    updated_at: int = int(datetime.timestamp(datetime.now()))