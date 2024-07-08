from fastapi import APIRouter, HTTPException
from models.messageModel import Message
from config.db_config import collection
from bson.objectid import ObjectId
from datetime import datetime
from jobs.messaging_job import send_message_job
from rq.job import Job
from redis import Redis
from schemas.messageSchema import all_messages_data, single_message_data

router = APIRouter(
    prefix="/api/v1",
    tags=["Message"],
    responses={404: {"description": "Not found"}},
)

redis_conn = Redis()

#messages routes
@router.get("/messages/")
async def get_messages():
    """
    Get all messages
    """
    data = collection["message"].find()
    return all_messages_data(data)

@router.get("/message/{message_id}")
async def get_single_message(message_id: str):
    """
    Get a single message
    """
    try:
        message_id = ObjectId(message_id)
        message = collection["message"].find_one({"_id": message_id})
        if message:
            return single_message_data(message)
        else:
            return HTTPException(status_code=404, detail=f"Message not found")
    except Exception as e:
        return HTTPException(status_code=500, detail=f"An error occurred: {e}")

@router.post("/message/")
async def create_message(message: Message):
    """
    Create a new message
    """
    try:
        result = collection["message"].insert_one(dict(message))
        message_sent = send_message_job(message)

        if message_sent:
            return {"status_code": 201, "id":str(result.inserted_id)}
        else:
            return {"status_code": 500, "message":"Message not sent"}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"An error occurred: {e}")

@router.put("/message/{message_id}")
async def update_message(message_id: str, updated_message: Message):
    """
    Update a message
    """
    try:
        message_id = ObjectId(message_id)
        existing_message = collection["message"].find_one({"_id": message_id})

        if not existing_message:
            return HTTPException(status_code=404, detail=f"Message not found")
        
        update_message.updated_at = datetime.timestamp(datetime.now())
        result = collection["message"].update_one({"_id": message_id}, {"$set":dict(updated_message)})
        return {"status_code": 200, "message":"Message Updated Successfully"}

    except Exception as e:
        return HTTPException(status_code=500, detail=f"An error occured {e}")

@router.delete("/message/{message_id}")
async def delete_message(message_id: str):
    """
    Delete a single message
    """
    try:
        message_id = ObjectId(message_id)
        existing_message = collection["message"].find_one({"_id": message_id})

        if not existing_message:
            return HTTPException(status_code=404, detail=f"Message not found")
        
        update_message.updated_at = datetime.timestamp(datetime.now())
        result = collection["message"].delete_one({"_id": message_id})
        return {"status_code": 200, "message":"Message Deleted Successfully"}

    except Exception as e:
        return HTTPException(status_code=500, detail=f"An error occured {e}")

@router.get("/message/live/{job_id}")
def get_live_messages(job_id: str):
    """
    Get messages from redis queue
    """
    try:
        job_ids = redis_conn.keys(f"rq:job:{job_id}*")
        messages = []

        for job_id in job_ids:
            job = Job.fetch(job_id.decode("utf-8").split(":")[-1], connection=redis_conn)
            if job.is_finished:
                message_data = job.result
                try:
                    if isinstance(message_data, dict):
                        message = Message(**message_data)
                        messages.append(message)
                        print(f"The message is: {messages}")
                    else:
                        raise HTTPException(status_code=500, detail="Invalid message format")
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"An error occurred in first block: {e}")
                redis_conn.delete(job_id)
            else:
                raise HTTPException(status_code=202, detail="Job is still running")

        return all_messages_data([msg for msg in messages])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred in last block: {e}")