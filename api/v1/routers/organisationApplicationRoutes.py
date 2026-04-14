"""
organisationApplicationRoutes module

CRUD operations for organisation applications.
All routes require authentication.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from bson.objectid import ObjectId
from bson.errors import InvalidId
from datetime import datetime

from models.organisationApplicationModel import OrganisationApplication as App
from models.userModel import User
from config.db_config import collection
from schemas.organisationApplicationSchema import all_apps_data, single_app_data
from auth.auth import get_current_active_user


router = APIRouter(
    prefix="/api/v1",
    tags=["App"],
    responses={404: {"description": "Not found"}},
)


def _parse_object_id(id_str: str) -> ObjectId:
    """Parse a string into ObjectId, raising HTTP 400 on invalid format."""
    try:
        return ObjectId(id_str)
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")


# ---------------------------------------------------------------------------
# GET /apps/ — list all apps (paginated)
# ---------------------------------------------------------------------------
@router.get("/apps/")
async def get_apps(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve a paginated list of all organisation applications.
    Requires authentication.
    """
    data = collection["app"].find().skip(skip).limit(limit)
    return all_apps_data(data)


# ---------------------------------------------------------------------------
# GET /app/{app_id} — single app
# ---------------------------------------------------------------------------
@router.get("/app/{app_id}")
async def get_single_app(
    app_id: str,
    current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve a single application by ID.
    Requires authentication.
    """
    oid = _parse_object_id(app_id)
    app = collection["app"].find_one({"_id": oid})
    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="App not found")
    return single_app_data(app)


# ---------------------------------------------------------------------------
# POST /app/ — create an app
# ---------------------------------------------------------------------------
@router.post("/app/", status_code=status.HTTP_201_CREATED)
async def create_app(
    app: App,
    current_user: User = Depends(get_current_active_user),
):
    """
    Create a new organisation application.
    Requires authentication.
    """
    try:
        # Verify the referenced organisation exists
        org_id = _parse_object_id(app.org_id)
        if not collection["org"].find_one({"_id": org_id}):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Referenced organisation does not exist",
            )

        result = collection["app"].insert_one(dict(app))
        return {"id": str(result.inserted_id)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {e}",
        )


# ---------------------------------------------------------------------------
# PUT /app/{app_id} — update an app
# ---------------------------------------------------------------------------
@router.put("/app/{app_id}")
async def update_app(
    app_id: str,
    updated_app: App,
    current_user: User = Depends(get_current_active_user),
):
    """
    Update an existing application by ID.
    Requires authentication.
    """
    try:
        oid = _parse_object_id(app_id)
        if not collection["app"].find_one({"_id": oid}):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="App not found")

        update_data = dict(updated_app)
        update_data["updated_at"] = int(datetime.timestamp(datetime.now()))
        collection["app"].update_one({"_id": oid}, {"$set": update_data})
        return {"message": "App updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {e}",
        )


# ---------------------------------------------------------------------------
# DELETE /app/{app_id} — delete an app
# ---------------------------------------------------------------------------
@router.delete("/app/{app_id}", status_code=status.HTTP_200_OK)
async def delete_app(
    app_id: str,
    current_user: User = Depends(get_current_active_user),
):
    """
    Delete an application by ID.
    Requires authentication.
    """
    try:
        oid = _parse_object_id(app_id)
        if not collection["app"].find_one({"_id": oid}):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="App not found")

        collection["app"].delete_one({"_id": oid})
        return {"message": "App deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {e}",
        )