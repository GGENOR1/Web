from typing import Any

from bson import ObjectId
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection

from DBConnection import get_db_collections
from massenges import UpdateUserModel, Users


def map_user(user: Any) -> Users:
    return Users(id=str(user["_id"]), Reputation=str(user['Reputation']), DisplayName=str(user["DisplayName"]), CreationDate=str(user['CreationDate']), LastAccessDate=str(user['LastAccessDate']))


def get_filter(id: str) -> dict:
    return {'_id': ObjectId(id)}


class UserRepository:
    _db_collection: AsyncIOMotorCollection

    def __init__(self, db_collection: AsyncIOMotorCollection):
        self._db_collection = db_collection

    async def create(self, user: UpdateUserModel) -> str:
        insert_result = await self._db_collection.insert_one(dict(user))
        return str(insert_result.inserted_id)

    async def update(self, user_id: str, user: UpdateUserModel) -> Any:
        db_student = await self._db_collection.find_one_and_replace(get_filter(user_id), dict(user))
        return map_user(db_student)

    async def get_user_by_id(self, user_id: str) -> Any:
        db_student = await self._db_collection.find_one(get_filter(user_id))
        return map_user(db_student)

    async def find_all(self) -> list[Users]:
        db_users = []
        async for user in self._db_collection.find():
            db_users.append(map_user(user))
        return db_users

    @staticmethod
    def get_instance(db_collection: AsyncIOMotorCollection = Depends(get_db_collections)):
        return UserRepository(db_collection)
