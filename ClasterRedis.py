# import asyncio
# import asyncredis
#
# async def main():
#      redis = await asyncredis.# connect to your redis server
#      await redis.set("val", "fal") # set a key called "hello" with a value of "world"
#      value = await redis.get("val") # retrieve the same key back from the database
#      print(value)
#       # close and terminate the connection
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
import asyncio
import os

import aioredis_cluster
from fastapi import Depends


# async def main():
#      redis = await aioredis_cluster.create_redis_cluster([
#           ("127.0.0.1", 6380),
#      ])
#      redis.setex()


# def __init__(self, startup_nodes):
#     self.redis = None
#     self.startup_nodes = startup_nodes
#
# async def connect(self):
#     self.redis = await aioredis_cluster.create_redis_cluster(self.startup_nodes)
#
# async def disconnect(self):
#     if self.redis:
#         self.redis.close()
#         await self.redis.wait_closed()
#
# async def lock_cache(self, key, timeout=10):
#     lock_key = f"lock:{key}"
#     acquired = await self.redis.set(lock_key, "locked", expire=timeout, exist="SET_IF_NOT_EXIST")
#     return acquired
#
# async def unlock_cache(self, key):
#     lock_key = f"lock:{key}"
#     await self.redis.delete(lock_key)
#
# async def get(self, key):
#     return await self.redis.get(key, encoding='utf-8')
#
# async def set(self, key, value):
#     return await self.redis.set(key, value)


import aioredis_cluster


class RedisManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'redis'):
            self.redis = None

    async def connect(self):
        if self.redis is None:
            print(os.getenv("REDIS_URL"))
            try:
                self.redis = await aioredis_cluster.create_redis_cluster([
                    (os.getenv("REDIS_URL")),
                    # Добавьте остальные узлы вашего кластера здесь, если нужно
                ])
                print("Connected to Redis Cluster")
                print(f"ааааааааааааааааааааааааааааааааааааааааааааа    {self.redis}")
            except Exception as e:
                print(f"Failed to connect to Redis Cluster: {e}, тут")

    async def disconnect(self):
        if self.redis:
            self.redis.close()
            await self.redis.wait_closed()
            print("Disconnected from Redis Cluster")

    async def lock_cache(self, key, timeout=10):
        lock_key = f"lock:{key}"
        acquired = await self.redis.set(lock_key, "locked", expire=timeout, exist="SET_IF_NOT_EXIST")
        return acquired

    async def get(self, key):
        try:
            value = await self.redis.get(key, encoding='utf-8')
            return value
        except Exception as e:
            print(f"Failed to get value from Redis: {e}")
            return None

    async def unlock_cache(self, key):
        try:
            value = await self.redis.delete(key)
            return value
        except Exception as e:
            print(f"Failed to delete key: {e}")
            return None
    async def set(self, key, value):
        try:
            await self.redis.set(key, value)
            print(f"Set value {value} for key {key} in Redis")
        except Exception as e:
            print(f"Failed to set value in Redis: {e}")

    async def setex(self, key, time, value):
        try:
            await (self.redis.setex(key, time, value))
            return value
        except Exception as e:
            print(f"Failed to setnx value in Redis: {e}")
