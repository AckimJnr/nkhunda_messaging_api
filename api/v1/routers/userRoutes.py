from fastapi import APIRouter, HTTPException
from bson.objectid import ObjectId
from datetime import datetime
from models.userModel import User
from config.db_config import collection
from schemas.userSchema import all_users_data, single_user_data
from auth.auth import get_current_user, get_password_hash


router = APIRouter(
    prefix="/api/v1",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)

# user routers
@router.get("/users/")
async def get_users():
    """
    Get all users
    """
    data = collection["user"].find()
    return all_users_data(data)

@router.get("/user/{user_id}")
async def get_single_user(user_id: str):
    """
    Get a single user
    """
    try:
        user_id = ObjectId(user_id)
        user = collection["user"].find_one({"_id": user_id})
        if user:
            return single_user_data(user)
        else:
            return HTTPException(status_code=404, detail=f"User not found")
    except Exception as e:
        return HTTPException(status_code=500, detail=f"An error occurred: {e}")

@router.post("/user/")
async def create_user(user: User):
    """
    Create a new user
    """
    try:
        hashed_password = get_password_hash(user.password)
        user_dict = dict(user)
        user_dict["password"] = hashed_password
        
        result = collection["user"].insert_one(dict(user_dict))
        return {"status_code": 201, "id":str(result.inserted_id)}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"An error occurred: {e}")

@router.put("/user/{user_id}")
async def update_user(user_id: str, updated_user: User):
    """
    Update a user
    """
    try:
        user_id = ObjectId(user_id)
        existing_user = collection["user"].find_one({"_id": user_id})

        if not existing_user:
            return HTTPException(status_code=404, detail=f"User not found")
        
        update_user.updated_at = datetime.timestamp(datetime.now())
        result = collection["user"].update_one({"_id": user_id}, {"$set":dict(updated_user)})
        return {"status_code": 200, "message":"User Updated Successfully"}

    except Exception as e:
        return HTTPException(status_code=500, detail=f"An error occured {e}")


@router.delete("/user/{user_id}")
async def delete_user(user_id: str):
    """
    Delete a single user
    """
    try:
        user_id = ObjectId(user_id)
        existing_user = collection["user"].find_one({"_id": user_id})

        if not existing_user:
            return HTTPException(status_code=404, detail=f"User not found")
        
        update_user.updated_at = datetime.timestamp(datetime.now())
        result = collection["user"].delete_one({"_id": user_id})
        return {"status_code": 200, "message":"User Deleted Successfully"}

    except Exception as e:
        return HTTPException(status_code=500, detail=f"An error occured {e}")
