from typing import Any

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pymongo import MongoClient

from DBConnection import db_client, get_db_collections
from massenges import Message

router = APIRouter()
message: list[Message] = []

def map_message(message: Any) -> Message:
    return Message(id=str(message["_id"]), text=message["DisplayName"])


@router.get("/")
async def get_all_mess(db_collection: AsyncIOMotorClient = Depends(get_db_collections)) -> list[Message]:
    db_message = []
    async for message in db_collection.find():
        db_message.append(map_message((message)))
    return db_message

@router.get("/hello2/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}!"}


# # Создаем экземпляр класса-сервиса MongoDB
# message_service = MessageService(db_client, "test", "testuser")
#
# # Маршрут для сохранения сообщения
# @router.post("/api/messages")
# def create_message(message: Message):
#     message_service.save_message(message)
#     return {"message": "Message saved"}
#
# @router.get("/api/messages/{id}")
# def find_create_message(id: str):
#     return {message_service.find_message(id)}
# print("hellow")