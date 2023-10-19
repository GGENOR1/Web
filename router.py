from typing import Any

from bson import ObjectId
from fastapi import APIRouter, Depends, status
from fastapi.openapi.models import Response
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pymongo import MongoClient

from DBConnection import db_client, get_db_collections
from massenges import Users

router = APIRouter()
message: list[Users] = []


def map_user(user: Any) -> Users:
    return Users(id=str(user["_id"]), creationDate=str(user['CreationDate']))


def get_filter(id: str) -> dict:
    return {'_id': ObjectId(id)}


# вывод всех пользователей
@router.get("/")
async def get_all_mess(db_collection: AsyncIOMotorClient = Depends(get_db_collections)) -> list[Users]:
    db_users = []
    async for user in db_collection.find():
        db_users.append(map_user(user))
    return db_users


# поиск по id пользоватлей
@router.get("/{user_id}", response_model=Users)
async def get_by_id(user_id: str, db_collection: AsyncIOMotorClient = Depends(get_db_collections)) -> Any:
    if not ObjectId.is_valid(user_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    db_user = await db_collection.find_one((get_filter(user_id)))

    if db_user is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return map_user(db_user)


#########################пофиксить неработающие коды ошибок

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
