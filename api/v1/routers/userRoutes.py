"""
userRoutes module

CRUD operations for users.
- POST /user/      — public (registration)
- All other routes — require authentication
"""

from fastapi import APIRouter, HTTPException, Depends, status
from bson.objectid import ObjectId
from bson.errors import InvalidId
from datetime import datetime

from models.userModel import User, UserCreate, UserUpdate
from config.db_config import collection
from schemas.userSchema import all_users_data, single_user_data
from auth.auth import get_current_active_user, get_password_hash


router = APIRouter(
    prefix="/api/v1",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)


def _parse_object_id(id_str: str) -> ObjectId:
    """Parse a string into ObjectId, raising HTTP 400 on invalid format."""
    try:
        return ObjectId(id_str)
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")


# ---------------------------------------------------------------------------
# GET /users/ — list all users (paginated)
# ---------------------------------------------------------------------------
@router.get("/users/")
async def get_users(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve a paginated list of all users.
    Requires authentication.
    """
    data = collection["user"].find().skip(skip).limit(limit)
    return all_users_data(data)


# ---------------------------------------------------------------------------
# GET /user/{user_id} — single user
# ---------------------------------------------------------------------------
@router.get("/user/{user_id}")
async def get_single_user(
    user_id: str,
    current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve a single user by ID.
    Requires authentication.
    """
    oid = _parse_object_id(user_id)
    user = collection["user"].find_one({"_id": oid})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return single_user_data(user)


# ---------------------------------------------------------------------------
# POST /user/ — create user (public registration endpoint)
# ---------------------------------------------------------------------------
@router.post("/user/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """
    Register a new user.
    The plain-text password is hashed before storage — it is never persisted in plain text.
    """
    try:
        # Check for duplicate email
        if collection["user"].find_one({"email": user.email}):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email already exists",
            )

        now = int(datetime.timestamp(datetime.now()))
        user_doc = {
            "full_name": user.full_name,
            "email": user.email,
            "hashed_password": get_password_hash(user.password),
            "role": user.role,
            "created_at": now,
            "updated_at": now,
        }
        result = collection["user"].insert_one(user_doc)
        return {"id": str(result.inserted_id)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {e}",
        )


# ---------------------------------------------------------------------------
# PUT /user/{user_id} — update user
# ---------------------------------------------------------------------------
@router.put("/user/{user_id}")
async def update_user(
    user_id: str,
    updated_user: UserUpdate,
    current_user: User = Depends(get_current_active_user),
):
    """
    Update an existing user.
    Only supplied fields are changed. If 'password' is provided it will be hashed.
    Requires authentication.
    """
    try:
        oid = _parse_object_id(user_id)
        if not collection["user"].find_one({"_id": oid}):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        update_data = {k: v for k, v in updated_user.model_dump().items() if v is not None}

        # Hash password if it was supplied
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

        update_data["updated_at"] = int(datetime.timestamp(datetime.now()))
        collection["user"].update_one({"_id": oid}, {"$set": update_data})
        return {"message": "User updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {e}",
        )


# ---------------------------------------------------------------------------
# DELETE /user/{user_id} — delete user
# ---------------------------------------------------------------------------
@router.delete("/user/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: str,
    current_user: User = Depends(get_current_active_user),
):
    """
    Delete a user by ID.
    Requires authentication.
    """
    try:
        oid = _parse_object_id(user_id)
        if not collection["user"].find_one({"_id": oid}):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        collection["user"].delete_one({"_id": oid})
        return {"message": "User deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {e}",
        )
