import os

from pymemcache import HashClient, Client

from Cache.json_serialaizer import JsonSerializer

memcached_client: Client = None

def get_memcached_clinet() -> Client:
    return memcached_client

def init_memcached_connection():
    global memcached_client
    memcached_URI = "localhost:11211,localhost:11212,localhost:11213"
    try:

        memcached_client = HashClient(memcached_URI.split(","), serde=JsonSerializer())
        print(f"Connection to memcached with uri {memcached_URI}")
    except Exception as EX:
        print(f"{EX}")


def close_memcached_connection():
    global memcached_client
    if memcached_client is None:
        return
    memcached_client.close()
