#!/usr/bin/env python3

from rq import Worker, Queue, Connection
from redis import Redis
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

listen = ['nkhunda_message_queue']

redis_conn = Redis()

if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker(list(map(Queue, listen)))
        logger.info("Starting worker...")
        worker.work()
