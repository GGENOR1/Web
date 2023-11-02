from typing import Any

from bson import ObjectId
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection

from DBConnection import get_db_collections_mess
from MessangeClass import Messages


def map_messages(mess: Any) -> Messages:
    id = str(mess.get("_id", ""))
    PostTypeId = str(mess.get("PostTypeId", ''))
    AcceptedAnswerId = str(mess.get("AcceptedAnswerId", ''))
    CreationDate = str(mess.get("CreationDate", ''))
    Score = str(mess.get("Score", ''))
    ViewCount = str(mess.get("ViewCount", ''))
    Body = str(mess.get("Body", ''))
    OwnerUserId = str(mess.get("OwnerUserId", ''))
    LastActivityDate = str(mess.get("LastActivityDate", ''))
    Title = str(mess.get("Title", ''))
    Tags = str(mess.get("Tags", ''))
    AnswerCount = str(mess.get("AnswerCount", ''))
    CommentCount = str(mess.get("CommentCount", ''))
    ContentLicense = str(mess.get("ContentLicense", ''))
    LastEditorUserId = str(mess.get("LastEditorUserId", ''))
    LastEditDate = str(mess.get("LastEditDate", ''))
    return Messages(id=id, PostTypeId=PostTypeId,
                    AcceptedAnswerId=AcceptedAnswerId,
                    CreationDate=CreationDate,
                    Score=Score, ViewCount=ViewCount, Body=Body,
                    OwnerUserId=OwnerUserId, LastActivityDate=LastActivityDate,
                    Title=Title, Tags=Tags, AnswerCount=AnswerCount, CommentCount=CommentCount,
                    ContentLicense=ContentLicense, LastEditorUserId=LastEditorUserId, LastEditDate=LastEditDate
                    )


def get_filter(id: str) -> dict:
    return {'_id': ObjectId(id)}


class MessageRepository:
    _db_collection: AsyncIOMotorCollection

    def __init__(self, db_collection: AsyncIOMotorCollection):
        self._db_collection = db_collection

    async def find_all(self) -> list[Messages]:
        db_mess = []
        async for mes in self._db_collection.find():
            db_mess.append(map_messages(mes))
        return db_mess


    @staticmethod
    def get_instance(db_collection: AsyncIOMotorCollection = Depends(get_db_collections_mess)):
        return MessageRepository(db_collection)
