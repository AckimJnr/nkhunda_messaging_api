from pydantic import BaseModel
from datetime import datetime
"""
app module
A model of an application requesting a messaging service
"""

class OrganisationApplication(BaseModel):
    """
    Implements an organisations application
    """
    org_id: str
    app_name: str
    app_type: str
    app_description: str
    created_at: int = int(datetime.timestamp(datetime.now()))
    updated_at: int = int(datetime.timestamp(datetime.now()))