import motor
from motor.motor_asyncio import AsyncIOMotorClient

db_client: AsyncIOMotorClient = None


async def connect_and_init_db():
    global db_client
    mongo_url = "mongodb://localhost:27017/"
    try:
        db_client = AsyncIOMotorClient(mongo_url)
        print("Successful connection")
    except Exception as ex:
        print(f"Cant connection {ex}")


async def close_connect():
    global db_client
    if db_client is None:
        print("Connection close")
        return
    else:
        db_client.close()