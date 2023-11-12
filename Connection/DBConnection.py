import os

import motor
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from dotenv import load_dotenv
load_dotenv()
db_client: AsyncIOMotorClient = None
print(str(os.getenv("MONGO_DB")))

async def get_db_collections_user() -> AsyncIOMotorCollection:
    mongo_db = (os.getenv('MONGO_DB'))
    mongo_collection = (os.getenv('MONGO_COLLECTION_USER'))
    print(mongo_collection)
    return db_client[mongo_db][mongo_collection]

async def get_db_collections_mess() -> AsyncIOMotorCollection:
    mongo_db = os.getenv('MONGO_DB')
    mongo_collection = os.getenv('MONGO_COLLECTION_MESSAGE')
    print (mongo_collection)
    return db_client[mongo_db][mongo_collection]

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