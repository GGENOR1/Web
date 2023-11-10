import os

import motor
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

db_client: AsyncIOMotorClient = None


async def get_db_collections_user() -> AsyncIOMotorCollection:
    db_name = "User"
    collections = "UserCollections"
    return db_client[db_name][collections]

async def get_db_collections_mess() -> AsyncIOMotorCollection:
    db_name = "User"
    collections = "Mess"
    return db_client[db_name][collections]

async def connect_and_init_db():
    global db_client
    mongo_url = os.getenv('MONGO_URI')
    try:
        db_client = AsyncIOMotorClient(mongo_url)
        print("Successful connection")
        print(mongo_url)
    except Exception as ex:
        print(f"Cant connection {ex}")
        print(mongo_url)


async def close_connect():
    global db_client
    if db_client is None:
        print("Connection close")
        return
    else:
        db_client.close()