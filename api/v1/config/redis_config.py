"""
redis_config module

Provides a single, shared Redis connection instance used across
the application (routers, jobs, workers) to avoid duplicated connections.
"""

from redis import Redis
from config.settings import settings

redis_conn = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
