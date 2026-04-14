"""
messageRoutes module

CRUD operations for messages plus a live job-status endpoint.
All routes require authentication.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from bson.objectid import ObjectId
from bson.errors import InvalidId
from datetime import datetime

from models.messageModel import Message
from models.userModel import User
from config.db_config import collection
from config.redis_config import redis_conn
from schemas.messageSchema import all_messages_data, single_message_data
from jobs.messaging_job import send_message_job
from auth.auth import get_current_active_user
from rq.job import Job


router = APIRouter(
    prefix="/api/v1",
    tags=["Message"],
    responses={404: {"description": "Not found"}},
)


def _parse_object_id(id_str: str) -> ObjectId:
    """Parse a string into ObjectId, raising HTTP 400 on invalid format."""
    try:
        return ObjectId(id_str)
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")


# ---------------------------------------------------------------------------
# GET /messages/ — list all messages (paginated)
# ---------------------------------------------------------------------------
@router.get("/messages/")
async def get_messages(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve a paginated list of all messages.
    Requires authentication.
    """
    data = collection["message"].find().skip(skip).limit(limit)
    return all_messages_data(data)


# ---------------------------------------------------------------------------
# GET /message/{message_id} — single message
# ---------------------------------------------------------------------------
@router.get("/message/{message_id}")
async def get_single_message(
    message_id: str,
    current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve a single message by ID.
    Requires authentication.
    """
    oid = _parse_object_id(message_id)
    message = collection["message"].find_one({"_id": oid})
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
    return single_message_data(message)


# ---------------------------------------------------------------------------
# POST /message/ — create and enqueue a message
# ---------------------------------------------------------------------------
@router.post("/message/", status_code=status.HTTP_201_CREATED)
async def create_message(
    message: Message,
    current_user: User = Depends(get_current_active_user),
):
    """
    Persist a new message and enqueue it for asynchronous delivery.
    Requires authentication.
    """
    try:
        result = collection["message"].insert_one(dict(message))
        message_sent = send_message_job(message)
        if not message_sent:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Message saved but could not be enqueued for delivery",
            )
        return {"id": str(result.inserted_id)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {e}",
        )


# ---------------------------------------------------------------------------
# PUT /message/{message_id} — update a message
# ---------------------------------------------------------------------------
@router.put("/message/{message_id}")
async def update_message(
    message_id: str,
    updated_message: Message,
    current_user: User = Depends(get_current_active_user),
):
    """
    Update an existing message by ID.
    Requires authentication.
    """
    try:
        oid = _parse_object_id(message_id)
        if not collection["message"].find_one({"_id": oid}):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")

        update_data = dict(updated_message)
        update_data["updated_at"] = int(datetime.timestamp(datetime.now()))
        collection["message"].update_one({"_id": oid}, {"$set": update_data})
        return {"message": "Message updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {e}",
        )


# ---------------------------------------------------------------------------
# DELETE /message/{message_id} — delete a message
# ---------------------------------------------------------------------------
@router.delete("/message/{message_id}", status_code=status.HTTP_200_OK)
async def delete_message(
    message_id: str,
    current_user: User = Depends(get_current_active_user),
):
    """
    Delete a single message by ID.
    Requires authentication.
    """
    try:
        oid = _parse_object_id(message_id)
        if not collection["message"].find_one({"_id": oid}):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")

        collection["message"].delete_one({"_id": oid})
        return {"message": "Message deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {e}",
        )


# ---------------------------------------------------------------------------
# GET /message/live/{job_id} — poll job status from Redis queue
# ---------------------------------------------------------------------------
@router.get("/message/live/{job_id}")
def get_live_messages(
    job_id: str,
    current_user: User = Depends(get_current_active_user),
):
    """
    Poll the Redis queue for completed message jobs matching job_id.
    Returns 202 while jobs are still processing; 200 with results when done.
    Requires authentication.
    """
    try:
        job_keys = redis_conn.keys(f"rq:job:{job_id}*")
        messages = []

        for job_key in job_keys:
            job_key_str = job_key.decode("utf-8").split(":")[-1]
            try:
                job = Job.fetch(job_key_str, connection=redis_conn)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Could not fetch job {job_key_str}: {e}",
                )

            if not job.is_finished:
                return JSONResponse(
                    status_code=status.HTTP_202_ACCEPTED,
                    content={"message": "Job is still processing", "job_id": job_key_str},
                )

            message_data = job.result
            if not isinstance(message_data, dict):
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Unexpected job result format for job {job_key_str}",
                )

            messages.append(message_data)
            redis_conn.delete(job_key)

        return messages

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {e}",
        )