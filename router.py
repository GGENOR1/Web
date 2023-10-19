from typing import Any

from bson import ObjectId
from fastapi import APIRouter, Depends, status
from fastapi.openapi.models import Response
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pydantic import BaseModel
from pymongo import MongoClient

from DBConnection import db_client, get_db_collections
from UserRepository import UserRepository
from massenges import Users, UpdateUserModel

router = APIRouter()
message: list[Users] = []


def map_user(user: Any) -> Users:
    return Users(id=str(user["_id"]), creationDate=str(user['CreationDate']))


def get_filter(id: str) -> dict:
    return {'_id': ObjectId(id)}


# вывод всех пользователей
@router.get("/")
async def get_all_users(repository: UserRepository = Depends(UserRepository.get_instance)) -> list[Users]:
    return await repository.find_all()


# поиск по id пользоватлей
@router.get("/{user_id}", response_model=Users)
async def get_by_id(user_id: str, repository: UserRepository = Depends(UserRepository.get_instance)) -> Any:
    if not ObjectId.is_valid(user_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    db_user = await repository.get_user_by_id(user_id)
    if db_user is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return db_user


@router.post("/")
async def add_user(user: UpdateUserModel,
                   repository: UserRepository = Depends(UserRepository.get_instance)) -> str:
    user_id = await repository.create(user)
    return user_id


@router.put("/{user_id}", response_model=Users)
async def update_user(user_id: str, user: UpdateUserModel, repository: UserRepository = Depends(UserRepository.get_instance)) -> Any:
    if not ObjectId.is_valid(user_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    db_user = await repository.update(user_id, user)
    if db_user is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return db_user



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
