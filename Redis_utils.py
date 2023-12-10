
# import aioredis_cluster
#
# redis_client = None
# global info
# async def connect_redis_and_init():
#     global redis_client, info
#     nodes =[("127.0.0.1", 6380)]
#     try:
#         redis_client =aioredis_cluster.create_redis_cluster(nodes)
#     except Exception as EX:
#         print(f"{EX}")
#
# async def close_memcached_connection():
#     global redis_client
#     if redis_client is None:
#         return
#     redis_client.close()

# def get_redis_client():
#     return redis_client



