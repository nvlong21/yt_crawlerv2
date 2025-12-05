from typing import Any
from ..models import *  # noqa: F403

from .db.database import Base
from .db.database import engine as engine


# -------------- database --------------
def create_tables() -> None:
    with engine.begin() as conn:
        Base.metadata.create_all(bind=conn)


# # -------------- cache --------------
# async def create_redis_cache_pool() -> None:
#     cache.pool = redis.ConnectionPool.from_url(settings.REDIS_CACHE_URL)
#     cache.client = redis.Redis.from_pool(cache.pool)  # type: ignore


# async def close_redis_cache_pool() -> None:
#     if cache.client is not None:
#         await cache.client.aclose()  # type: ignore


# # -------------- queue --------------
# async def create_redis_queue_pool() -> None:
#     queue.pool = await create_pool(RedisSettings(host=settings.REDIS_QUEUE_HOST, port=settings.REDIS_QUEUE_PORT))


# async def close_redis_queue_pool() -> None:
#     if queue.pool is not None:
#         await queue.pool.aclose()  # type: ignore