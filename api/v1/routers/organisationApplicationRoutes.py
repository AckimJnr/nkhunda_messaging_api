from fastapi import APIRouter, HTTPException
from bson.objectid import ObjectId
from datetime import datetime
from models.organisationApplicationModel import OrganisationApplication as App
from config.db_config import collection
from schemas.organisationApplicationSchema import all_apps_data, single_app_data


router = APIRouter(
    prefix="/api/v1",
    tags=["App"],
    responses={404: {"description": "Not found"}},
)


#app routes
@router.get("/apps/")
async def get_apps():
    """
    Get all apps
    """
    data = collection["app"].find()
    return all_apps_data(data)

@router.get("/app/{app_id}")
async def get_single_app(app_id: str):
    """
    Get a single app
    """
    try:
        app_id = ObjectId(app_id)
        app = collection["app"].find_one({"_id": app_id})
        if app:
            return single_app_data(app)
        else:
            return HTTPException(status_code=404, detail=f"App not found")
    except Exception as e:
        return HTTPException(status_code=500, detail=f"An error occurred: {e}")

@router.post("/app/")
async def create_app(app: App):
    """
    Create a new app
    """
    try:
        result = collection["app"].insert_one(dict(app))
        return {"status_code": 201, "id":str(result.inserted_id)}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
@router.put("/app/{app_id}")
async def update_app(app_id: str, updated_app: App):
    """
    Update an app
    """
    try:
        app_id = ObjectId(app_id)
        existing_app = collection["app"].find_one({"_id": app_id})

        if not existing_app:
            return HTTPException(status_code=404, detail=f"App not found")
        
        update_app.updated_at = datetime.timestamp(datetime.now())
        result = collection["app"].update_one({"_id": app_id}, {"$set":dict(updated_app)})
        return {"status_code": 200, "message":"App Updated Successfully"}

    except Exception as e:
        return HTTPException(status_code=500, detail=f"An error occured {e}")

@router.delete("/app/{app_id}")
async def delete_app(app_id: str):
    """
    Delete a single app
    """
    try:
        app_id = ObjectId(app_id)
        existing_app = collection["app"].find_one({"_id": app_id})

        if not existing_app:
            return HTTPException(status_code=404, detail=f"App not found")
        
        update_app.updated_at = datetime.timestamp(datetime.now())
        result = collection["app"].delete_one({"_id": app_id})
        return {"status_code": 200, "message":"App Deleted Successfully"}

    except Exception as e:
        return HTTPException(status_code=500, detail=f"An error occured {e}")