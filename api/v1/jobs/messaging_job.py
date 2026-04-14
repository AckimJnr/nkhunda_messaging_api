"""
messaging_job module

Enqueues message processing jobs onto the shared Redis queue.
Uses the centralised redis_conn from config.redis_config.
"""

from models.messageModel import Message
from rq import Queue
from config.redis_config import redis_conn
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

q = Queue("nkhunda_message_queue", connection=redis_conn)


def send_message_job(message: Message) -> bool:
    """
    Enqueues a message processing job.
    Returns True on success, False on failure.
    """
    try:
        timestamp = int(time.time() * 1000)
        job_id = f"{message.app_id}-{message.recipient_id}-{timestamp}"
        q.enqueue("workers.message_worker.send_message", dict(message), job_id=job_id)
        logger.info(f"Enqueued message job with id: {job_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to enqueue message job: {e}")
        return False
