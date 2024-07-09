from models.messageModel import Message
from rq import Queue
from redis import Redis
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

redis_conn = Redis()
q = Queue("nkhunda_message_queue", connection=redis_conn)

def send_message_job(message: Message) :
    """
    Send message job
    """
    try:
        timestamp = int(time.time() * 1000)
        job_id = f"{message.app_id}-{message.recipient_id}-{timestamp}"
        job = q.enqueue("workers.message_worker.send_message", dict(message), job_id=job_id)
        logger.info(f"Enqueued job with id {job_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to enqueue job: {e}")
        return False
