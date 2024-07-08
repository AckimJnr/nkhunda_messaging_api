import os
from fastapi import APIRouter, HTTPException
from bson.objectid import ObjectId
from datetime import datetime
from models.organisationModel import Organisation as Org
from config.db_config import collection
from schemas.organisationSchema import all_orgs_data, single_org_data


router = APIRouter(
    prefix="/api/v1",
    tags=["Organisation"],
    responses={404: {"description": "Not found"}},
)


#organisaton routes
@router.get("/orgs/")
async def get_orgs():
    """
    Get all organisations
    """
    data = collection["org"].find()
    return all_orgs_data(data)

@router.get("/org/{org_id}")
async def get_single_org(org_id: str):
    """
    Get a single organisation
    """
    try:
        org_id = ObjectId(org_id)
        org = collection["org"].find_one({"_id": org_id})
        if org:
            return single_org_data(org)
        else:
            return HTTPException(status_code=404, detail=f"Organisation not found")
    except Exception as e:
        return HTTPException(status_code=500, detail=f"An error occurred: {e}")

@router.post("/org/")
async def create_org(org: Org):
    """
    Create a new organisation
    """
    try:
        result = collection["org"].insert_one(dict(org))
        return {"status_code": 201, "id":str(result.inserted_id)}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"An error occurred: {e}")

@router.put("/org/{org_id}")
async def update_org(org_id: str, updated_org: Org):
    """
    Update an organisation
    """
    try:
        org_id = ObjectId(org_id)
        existing_org = collection["org"].find_one({"_id": org_id})

        if not existing_org:
            return HTTPException(status_code=404, detail=f"Organisation not found")
        
        update_org.updated_at = datetime.timestamp(datetime.now())
        result = collection["org"].update_one({"_id": org_id}, {"$set":dict(updated_org)})
        return {"status_code": 200, "message":"Organisation Updated Successfully"}

    except Exception as e:
        return HTTPException(status_code=500, detail=f"An error occured {e}")

@router.delete("/org/{org_id}")
async def delete_org(org_id: str):
    """
    Delete a single organisation
    """
    try:
        org_id = ObjectId(org_id)
        existing_org = collection["org"].find_one({"_id": org_id})

        if not existing_org:
            return HTTPException(status_code=404, detail=f"Organisation not found")
        
        update_org.updated_at = datetime.timestamp(datetime.now())
        result = collection["org"].delete_one({"_id": org_id})
        return {"status_code": 200, "message":"Organisation Deleted Successfully"}

    except Exception as e:
        return HTTPException(status_code=500, detail=f"An error occured {e}")