import ast
import asyncio
import codecs
import json
import os
import pickle
import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
from typing import Any

# import aioredis as s
from bson import ObjectId
from fastapi import APIRouter, Depends, status
from pymemcache import HashClient
from pymongo import MongoClient
from starlette.responses import JSONResponse


from ClasterRedis import RedisManager
from Search.Message_Search_elastic import MessageSearchRepository
from Repository.MessagesRepository import MessageRepository
from Models.MessangeClass import Messages, UpdateMessagesModel
from Repository.UserRepository import UserRepository
from Search.User_Search_elastic import UserSearchRepository
from Models.UserClass import Users, UpdateUserModel

router = APIRouter()
message: list[Users] = []

# from rediscluster import RedisCluster
#
# # Requires at least one node for cluster discovery. Multiple nodes is recommended.
# startup_nodes = [{"host": "127.0.0.1", "port": "6380"}, {"host": "127.0.0.1", "port": "6381"}, {"host": "127.0.0.1", "port": "6382"},{"host": "127.0.0.1", "port": "6383"},
#                  {"host": "127.0.0.1", "port": "6384"},{"host": "127.0.0.1", "port": "6385"}]
# rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)


# вывод всех пользователей
@router.get("/user", tags=["Users"])
async def get_all_users(repository: UserRepository = Depends(UserRepository.get_instance)) -> list[Users]:
    return await repository.find_all()


# поиск по имени пользователя
@router.get("/user/search", tags=["Users"])
async def get_users(name: str, size:int=20, page:int=1, repository: UserSearchRepository = Depends(UserSearchRepository.get_instance)) -> \
        list[Users]:
    return await repository.get_by_name(name,size,page)


@router.get("/message/search/body", tags=["messages"])
async def get_string(string: str,
                     page:int = 1,
                     page_size: int = 20,
                     repository: MessageSearchRepository = Depends(MessageSearchRepository.get_instance)) -> \
        list[Messages]:
    return await repository.get_by_Body(string, page, page_size)


@router.get("/user/{user_id}", response_model=Users, tags=["Users"])
async def get_by_id(user_id: str,
                    repository: UserRepository = Depends(UserRepository.get_instance)) -> Any:
    await redis_manager.connect()
    if not ObjectId.is_valid(user_id):
        return JSONResponse(content={'status': 'BAD_REQUEST'}, status_code=status.HTTP_400_BAD_REQUEST)
    cache_key = f"{user_id}"
    cached_user_data = await redis_manager.get(cache_key)
    if cached_user_data:
        print(f"беру из кэша {cached_user_data}")

        return json.loads(cached_user_data)
    user = await repository.get_user_by_id(user_id)
    print(f"тут возвращает {user}")
    if not user:
        return JSONResponse(content={'status': 'NOT_FOUND'}, status_code=status.HTTP_404_NOT_FOUND)
    user_dict = user.dict()
    user_json = json.dumps(user_dict)

    await redis_manager.setex(cache_key, 60, user_json)
    return user

# добавление поользователя
@router.post("/user", tags=["Users"])
async def add_user(user: UpdateUserModel,
                   repository: UserRepository = Depends(UserRepository.get_instance),
                   search_repository: UserSearchRepository = Depends(UserSearchRepository.get_instance)) -> str:
    user_id = await repository.create(user)
    await search_repository.create(user_id, user)
    return user_id


@router.post("/message", tags=["messages"])
async def add_messages(message: UpdateMessagesModel,
                       repository: MessageRepository = Depends(MessageRepository.get_instance),
                       search_repository: MessageSearchRepository = Depends(MessageSearchRepository.get_instance)
                       ) -> str:
    mess_id = await repository.create_post(message)
    await search_repository.create(mess_id, message)
    return mess_id

redis_manager = RedisManager()


@router.put("/user/{user_id}", response_model=Users, tags=["Users"])
async def update_user(user_id: str,
                      user: UpdateUserModel,
                      repository: UserRepository = Depends(UserRepository.get_instance),
                      search_repository: UserSearchRepository = Depends(UserSearchRepository.get_instance),
                      ) -> Any:
    await redis_manager.connect()
    if not ObjectId.is_valid(user_id):
        return JSONResponse(content={'status': 'BAD_REQUEST'}, status_code=status.HTTP_400_BAD_REQUEST)
    lock_key = f"{user_id}"
    lock_acquired = await redis_manager.lock_cache(lock_key)
    if not lock_acquired:
        print(f"{lock_acquired} - заблокировано кем то другим")

        return JSONResponse(content={'status': 'CONFLICT'}, status_code=status.HTTP_409_CONFLICT)
    try:
        print(f"{lock_acquired} - блокировка установлена на данный момент")
        db_user = await repository.update(user_id, user)
        if not db_user:
            return JSONResponse(content={'status': 'NOT_FOUND'}, status_code=status.HTTP_404_NOT_FOUND)
        await search_repository.update(user_id, user)
        cache_key = f"{user_id}"
        print(f"тут возвращает {db_user}")
        user_dict = user.__dict__
        user_dict["id"] = user_id
        print(f"а кэшируется {json.dumps(user_dict)}")
        await redis_manager.setex(cache_key, 60, json.dumps(user_dict))
        return JSONResponse(content={'status': 'HTTP_200_OK'}, status_code=status.HTTP_200_OK)
    finally:
        if lock_acquired:
            await redis_manager.unlock_cache(lock_key)



@router.get("/message/synchronization/message", tags=["Admin"])
async def synchronization_Message(
        repository: MessageRepository = Depends(MessageRepository.get_instance),
        search_repository: MessageSearchRepository
        = Depends(MessageSearchRepository.get_instance),
) -> list[Messages]:
    page_size = 15000  # Размер страниц
    # Получаем данные пачками (страницами)
    page = 1
    messages = await repository.find_paginated(page,page_size)
    while messages:
        for mes in messages:
            print(mes)
            mes_without_id = {key: value for key, value in mes.dict().items() if key != 'id'}
            post = await search_repository.test_find(mes.id)
            if post:
                await search_repository.update(mes.id, mes_without_id)
            else:
                await search_repository.create(mes.id, mes_without_id)
        # Получаем следующую пачку данных
        page += 1
        messages = await repository.find_paginated(page, page_size)
    return JSONResponse(content={'status': 'GOOD'}, status_code=status.HTTP_200_OK)


@router.get("/message/synchronization/user", tags=["Admin"])
async def synchronization_User(
        repository: UserRepository = Depends(UserRepository.get_instance),
        search_repository: UserSearchRepository
        = Depends(UserSearchRepository.get_instance),
) -> list[Messages]:
    page_size = 15000
    #
    page = 1
    users = await repository.find_paginated(page,page_size)
    while users:
        for user in users:
            print(user)
            user_without_id = {key: value for key, value in user.dict().items() if key != 'id'}
            post = await search_repository.test_find(user.id)
            if post:
                await search_repository.update(user.id, user_without_id)
            else:
                await search_repository.create(user.id, user_without_id)
        # Получаем следующую пачку данных
        page += 1
        users = await repository.find_paginated(page, page_size)
    return JSONResponse(content={'status': 'GOOD'}, status_code=status.HTTP_200_OK)



@router.get("/message/", tags=["messages"])
async def get_all_message(repository: MessageRepository = Depends(MessageRepository.get_instance)) -> list[Messages]:
    return await repository.find_all()


@router.get("/message/{message_id}", tags=["messages"], response_model=Messages)
async def get_by_id(message_id: str,
                    repository: MessageRepository = Depends(MessageRepository.get_instance),
                   ) -> Any:
    if not ObjectId.is_valid(message_id):
        return JSONResponse(content={'status': 'BAD_REQUEST'}, status_code=status.HTTP_400_BAD_REQUEST)
    db_mess = await repository.find_mess_by_id(message_id)
    if db_mess is None:
        return JSONResponse(content={'status': 'NOT_FOUND'}, status_code=status.HTTP_404_NOT_FOUND)

    return db_mess


@router.put("/message/{message_id}", tags=["messages"], response_model=Messages)
async def update_messages(message_id: str,
                          message: UpdateMessagesModel,
                          repository: MessageRepository = Depends(MessageRepository.get_instance),
                          search_repository: MessageSearchRepository = Depends(MessageSearchRepository.get_instance)
                          ) -> Any:
    if not ObjectId.is_valid(message_id):
        return JSONResponse(content={'status': 'BAD_REQUEST'}, status_code=status.HTTP_400_BAD_REQUEST)
    db_mess = await repository.update_post(message_id, message)
    if db_mess is None:
        return JSONResponse(content={'status': 'NOT_FOUND'}, status_code=status.HTTP_404_NOT_FOUND)
    in_Es = await search_repository.test_find(message_id)

    if not in_Es:
        print(f"тут {in_Es}")
        await search_repository.create(message_id, message)
        return db_mess
    else:
        await search_repository.update(message_id, message)
    return db_mess

@router.get("/message/search/datecreated", tags=["messages"])
async def get_string(date1: str = "now-1d/d", date2: str = "now/d", size: int = 20, page:int=1,
                     repository: MessageSearchRepository = Depends(MessageSearchRepository.get_instance)) -> \
        list[Messages]:
    return await repository.get_by_date(date1, date2, size,page)

import xml.etree.ElementTree as ET

def parse_xml_row(row):
    mes_data = {
                                        'PostTypeId': int(row.get('PostTypeId', 0)),
                                        'AcceptedAnswerId': int(row.get('AcceptedAnswerId', 0)),
                                        'CreationDate': row.get('CreationDate', "1000-01-01"),
                                        "Score": int(row.get('Score', 0)),
                                        "ViewCount": int(row.get('ViewCount', 0)),
                                        'Body':codecs.encode(row.get('Body', ""), 'utf-8', 'ignore').decode('utf-8'),
                                        "OwnerUserId": int(row.get('OwnerUserId', 0)),
                                        'LastActivityDate': row.get('LastActivityDate', "1000-01-01"),
                                        'Title': codecs.encode(row.get('Title', ""), 'utf-8', 'ignore').decode('utf-8'),
                                        'Tags':codecs.encode(row.get('Tags', ""), 'utf-8', 'ignore').decode('utf-8'),
                                        "AnswerCount": int(row.get('AnswerCount', 0)),
                                        "CommentCount": int(row.get('CommentCount', 0)),
                                        'ContentLicense': row.get('ContentLicense', ""),
                                        "LastEditorUserId": int(row.get('LastEditorUserId', 0)),
                                        'LastEditDate': row.get('LastEditDate', "1000-01-01")
                        }
    return mes_data
@router.get("/message/search/PostInDB", tags=["Admin"])
def load_data_into_mongodb():
    xml_file = "Dump2/Posts2.xml"
    tree = ET.parse(xml_file)
    root = tree.getroot()
    rows = root.findall('row')
    batch_size = 20
    batches = [rows[i:i + batch_size] for i in range(0, len(rows), batch_size)]
    client = MongoClient(os.getenv('MONGO_URI'))
    db = client["USER2"]
    collection = db["Message"]
    for batch in batches:
        data_to_insert = [parse_xml_row(row) for row in batch]
        collection.insert_many(data_to_insert)



def parse_xml_row1(row):
    mes_data = {
        'Reputation': int(row.get('Reputation', 0)),
        'CreationDate': row.get('CreationDate', "1000-01-01"),
        'DisplayName': codecs.encode(row.get('DisplayName', ""), 'utf-8', 'ignore').decode('utf-8'),
        'LastAccessDate': row.get('LastAccessDate', "0000-00-00"),
        'WebsiteUrl': codecs.encode(row.get('WebsiteUrl', ""), 'utf-8', 'ignore').decode('utf-8'),
        'Location': row.get('Location', ""),
        'AboutMe': codecs.encode(row.get('AboutMe', ""), 'utf-8', 'ignore').decode('utf-8'),
        'Views': int(row.get('Views', 0)),
        'UpVotes': int(row.get('UpVotes', 0)),
        'DownVotes': int(row.get('DownVotes', 0)),
        'AccountId': row.get('AccountId', "-1"),
                        }
    return mes_data
@router.get("/message/search/UserInDB", tags=["Admin"])
def load_user_into_mongodb():
    xml_file = "Dump2/Users2.xml"
    tree = ET.parse(xml_file)
    root = tree.getroot()
    rows = root.findall('row')
    batch_size = 20
    batches = [rows[i:i + batch_size] for i in range(0, len(rows), batch_size)]
    client = MongoClient(os.getenv('MONGO_URI'))
    db = client["USER2"]
    collection = db["User"]
    for batch in batches:
        data_to_insert = [parse_xml_row1(row) for row in batch]

        collection.insert_many(data_to_insert)
