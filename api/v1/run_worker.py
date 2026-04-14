#!/usr/bin/env python3
"""
run_worker

Starts the RQ worker process that listens to the nkhunda_message_queue.
Run this separately from the API server:  python run_worker.py
Uses the centralised redis_conn from config.redis_config.
"""

from rq import Worker, Queue, Connection
from config.redis_config import redis_conn
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

listen = ["nkhunda_message_queue"]

if __name__ == "__main__":
    with Connection(redis_conn):
        worker = Worker(list(map(Queue, listen)))
        logger.info("Starting RQ worker, listening on: %s", listen)
        worker.work()
