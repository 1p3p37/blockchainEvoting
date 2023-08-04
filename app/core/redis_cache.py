import functools
import logging
import json
import aioredis

from app.core.config import settings


# Asynchronous Redis connection
async def get_redis_connection():
    return await aioredis.from_url(
        settings.redis_url,
        encoding="utf-8",
        decode_responses=True,
    )


# Async cache decorator
def cache_response(ttl: int = 60):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            redis_client = await get_redis_connection()
            # Generate a cache key based on the function arguments
            cache_key = f"{func.__name__}:{str(args)},{str(kwargs)}"
            cached_response = await redis_client.get(cache_key)
            if cached_response:
                response = json.loads(cached_response)
            else:
                response = await func(*args, **kwargs)
                logging.info(f"Cached response with {ttl} ttl: {response}")

                await redis_client.setex(cache_key, ttl, json.dumps(response))
            # redis_client.close()
            # await redis_client.wait_closed()
            return response

        return wrapper

    return decorator


"""
Not aio
"""
# import redis
# import pickle

# redis_client = redis.StrictRedis(
#     host=settings.redis_host, port=settings.redis_port, db=0, decode_responses=True
# )


# async def cache_response(ttl):
#     def decorator(func):
#         @functools.wraps(func)
#         async def wrapper(*args, **kwargs):
#             # Generate a cache key based on the function arguments
#             cache_key = f"{func.__name__}:{str(args)},{str(kwargs)}"
#             cached_response = await redis_client.get(cache_key)
#             if cached_response:
#                 return json.loads(cached_response)
#             response = await func(*args, **kwargs)
#             await redis_client.setex(cache_key, ttl, json.dumps(response))
#             return response

#         return wrapper

#     return decorator
