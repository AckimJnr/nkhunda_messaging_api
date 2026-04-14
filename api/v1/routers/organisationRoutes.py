"""
organisationRoutes module

CRUD operations for organisations.
All routes require authentication.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from bson.objectid import ObjectId
from bson.errors import InvalidId
from datetime import datetime

from models.organisationModel import Organisation as Org
from models.userModel import User
from config.db_config import collection
from schemas.organisationSchema import all_orgs_data, single_org_data
from schemas.organisationApplicationSchema import all_apps_data
from auth.auth import get_current_active_user


router = APIRouter(
    prefix="/api/v1",
    tags=["Organisation"],
    responses={404: {"description": "Not found"}},
)


def _parse_object_id(id_str: str) -> ObjectId:
    """Parse a string into ObjectId, raising HTTP 400 on invalid format."""
    try:
        return ObjectId(id_str)
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")


# ---------------------------------------------------------------------------
# GET /orgs/ — list all organisations with their apps (paginated)
# ---------------------------------------------------------------------------
@router.get("/orgs/")
async def get_orgs(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve a paginated list of all organisations, each including their apps.
    Requires authentication.
    """
    try:
        orgs = collection["org"].find().skip(skip).limit(limit)
        orgs_data = []
        for org in orgs:
            org_id = str(org["_id"])
            apps = collection["app"].find({"org_id": org_id})
            org_data = single_org_data(org)
            org_data["apps"] = all_apps_data(apps)
            orgs_data.append(org_data)
        return orgs_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {e}",
        )


# ---------------------------------------------------------------------------
# GET /org/{org_id} — single organisation with its apps
# ---------------------------------------------------------------------------
@router.get("/org/{org_id}")
async def get_single_org(
    org_id: str,
    current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve a single organisation by ID, including its apps.
    Requires authentication.
    """
    try:
        oid = _parse_object_id(org_id)
        org = collection["org"].find_one({"_id": oid})
        if not org:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organisation not found")

        apps = collection["app"].find({"org_id": str(oid)})
        org_data = single_org_data(org)
        org_data["apps"] = all_apps_data(apps)
        return org_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {e}",
        )


# ---------------------------------------------------------------------------
# POST /org/ — create an organisation
# ---------------------------------------------------------------------------
@router.post("/org/", status_code=status.HTTP_201_CREATED)
async def create_org(
    org: Org,
    current_user: User = Depends(get_current_active_user),
):
    """
    Create a new organisation.
    The 'owner' field must be a valid existing user ID.
    Requires authentication.
    """
    try:
        owner_id = _parse_object_id(org.owner)
        if not collection["user"].find_one({"_id": owner_id}):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Owner user does not exist",
            )

        result = collection["org"].insert_one(dict(org))
        return {"id": str(result.inserted_id)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {e}",
        )


# ---------------------------------------------------------------------------
# PUT /org/{org_id} — update an organisation
# ---------------------------------------------------------------------------
@router.put("/org/{org_id}")
async def update_org(
    org_id: str,
    updated_org: Org,
    current_user: User = Depends(get_current_active_user),
):
    """
    Update an existing organisation by ID.
    Requires authentication.
    """
    try:
        oid = _parse_object_id(org_id)
        if not collection["org"].find_one({"_id": oid}):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organisation not found")

        update_data = dict(updated_org)
        update_data["updated_at"] = int(datetime.timestamp(datetime.now()))
        collection["org"].update_one({"_id": oid}, {"$set": update_data})
        return {"message": "Organisation updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {e}",
        )


# ---------------------------------------------------------------------------
# DELETE /org/{org_id} — delete an organisation
# ---------------------------------------------------------------------------
@router.delete("/org/{org_id}", status_code=status.HTTP_200_OK)
async def delete_org(
    org_id: str,
    current_user: User = Depends(get_current_active_user),
):
    """
    Delete an organisation by ID.
    Requires authentication.
    """
    try:
        oid = _parse_object_id(org_id)
        if not collection["org"].find_one({"_id": oid}):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organisation not found")

        collection["org"].delete_one({"_id": oid})
        return {"message": "Organisation deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {e}",
        )