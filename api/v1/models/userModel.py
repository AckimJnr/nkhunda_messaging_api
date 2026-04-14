"""
userModel module

Contains User model variants:
- UserCreate  — used for registration (accepts a plain-text password)
- UserUpdate  — used for partial updates (all fields optional)
- User        — internal DB model (stores hashed_password, never exposed)
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    """
    Request body for creating a new user.
    Accepts a plain-text password that will be hashed before storage.
    """
    full_name: str
    email: str
    password: str
    role: str


class UserUpdate(BaseModel):
    """
    Request body for updating an existing user.
    All fields are optional — only supplied fields will be updated.
    Supply 'password' to change the password; it will be hashed before storage.
    """
    full_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None


class User(BaseModel):
    """
    Internal user model as stored in the database.
    Never expose hashed_password in API responses.
    """
    full_name: str
    email: str
    hashed_password: str
    role: str
    created_at: int = int(datetime.timestamp(datetime.now()))
    updated_at: int = int(datetime.timestamp(datetime.now()))