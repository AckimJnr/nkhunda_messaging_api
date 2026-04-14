"""
message_worker module

Processes messages dequeued from the Redis job queue.
Note: this function MUST be synchronous — RQ cannot execute async functions.
"""

import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_message(message_data: dict) -> dict:
    """
    Processes a message payload received from the RQ queue.
    Returns the processed message dict, or an error dict on failure.
    """
    try:
        logger.info(f"Processing message: {message_data}")
        message = {
            "app_id": message_data["app_id"],
            "message_type": message_data["message_type"],
            "group_id": message_data["group_id"],
            "status": message_data["status"],
            "message_content": message_data["message_content"],
            "sender_id": message_data["sender_id"],
            "recipient_id": message_data["recipient_id"],
            "created_at": message_data.get("created_at", int(datetime.timestamp(datetime.now()))),
            "updated_at": int(datetime.timestamp(datetime.now())),
        }
        logger.info(f"Message processed successfully: {message}")
        return message
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return {"status": "failure", "error": str(e)}
