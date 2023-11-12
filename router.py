from typing import Any

from bson import ObjectId
from fastapi import APIRouter, Depends, status
from pymemcache import HashClient
from starlette.responses import JSONResponse

from Cache.Memcached_utils import get_memcached_clinet
from Search.Message_Search_elastic import MessageSearchRepository
from Repository.MessagesRepository import MessageRepository
from Models.MessangeClass import Messages, UpdateMessagesModel
from Repository.UserRepository import UserRepository
from Search.User_Search_elastic import UserSearchRepository
from Models.UserClass import Users, UpdateUserModel

router = APIRouter()
message: list[Users] = []


# вывод всех пользователей
@router.get("/user")
async def get_all_users(repository: UserRepository = Depends(UserRepository.get_instance)) -> list[Users]:
    return await repository.find_all()


# поиск по имени пользователя
@router.get("/user/search")
async def get_all_users(name: str, repository: UserSearchRepository = Depends(UserSearchRepository.get_instance)) -> \
        list[Users]:
    return await repository.get_by_name(name)


@router.get("/message/search/body")
async def get_string(string: str,
                     repository: MessageSearchRepository = Depends(MessageSearchRepository.get_instance)) -> \
        list[Messages]:
    return await repository.get_by_Body(string)


@router.get("/message/search/datecreated")
async def get_string(date1: str = "now-1d/d", date2: str = "now/d",
                     repository: MessageSearchRepository = Depends(MessageSearchRepository.get_instance)) -> \
        list[Messages]:
    return await repository.get_by_date(date1, date2)


# поиск по id пользоватлей
@router.get("/user/{user_id}", response_model=Users)
async def get_by_id(user_id: str,
                    repository: UserRepository = Depends(UserRepository.get_instance),
                    memcahed_clien: HashClient = Depends(get_memcached_clinet)) -> Any:
    if not ObjectId.is_valid(user_id):
        return JSONResponse(content={'status': 'BAD_REQUEST'}, status_code=status.HTTP_400_BAD_REQUEST)

    user = memcahed_clien.get(user_id)
    # print(user)
    if user is not None:
        print(user)
        return user

    user = await repository.get_user_by_id(user_id)
    if user is None:
        return JSONResponse(content={'status': 'NOT_FOUND'}, status_code=status.HTTP_404_NOT_FOUND)
    memcahed_clien.add(user_id, user)
    return user


# добавление поользователя
@router.post("/user")
async def add_user(user: UpdateUserModel,
                   repository: UserRepository = Depends(UserRepository.get_instance),
                   search_repository: UserSearchRepository = Depends(UserSearchRepository.get_instance)) -> str:
    user_id = await repository.create(user)
    await search_repository.create(user_id, user)
    return user_id


@router.post("/message")
async def add_messages(message: UpdateMessagesModel,
                       repository: MessageRepository = Depends(MessageRepository.get_instance),
                       search_repository: MessageSearchRepository = Depends(MessageSearchRepository.get_instance)
                       ) -> str:
    mess_id = await repository.create_post(message)
    await search_repository.create(mess_id, message)
    return mess_id


@router.put("/user/{user_id}", response_model=Users)
async def update_user(user_id: str,
                      user: UpdateUserModel,
                      repository: UserRepository = Depends(UserRepository.get_instance),
                      search_repository: UserSearchRepository = Depends(UserSearchRepository.get_instance)
                      ) -> Any:
    if not ObjectId.is_valid(user_id):
        return JSONResponse(content={'status': 'BAD_REQUEST'}, status_code=status.HTTP_400_BAD_REQUEST)
    db_user = await repository.update(user_id, user)
    if db_user is None:
        return JSONResponse(content={'status': 'NOT_FOUND'}, status_code=status.HTTP_404_NOT_FOUND)
    await search_repository.update(user_id, user)
    return db_user


##функция для синхронизации данных из mongodb в ES
@router.get("/message/synchronization")
async def synchronization_Data(
                               repository: MessageRepository = Depends(MessageRepository.get_instance),
                               search_repository: MessageSearchRepository
                               = Depends(MessageSearchRepository.get_instance)
                               ) -> list[Messages]:
    message = await repository.find_all()
    for mes in message:
        mes_without_id = {key: value for key, value in mes.dict().items() if key != 'id'}
        post = await search_repository.test_find(mes.id)
        if post:
            await search_repository.update(mes.id,mes_without_id)
        else:
            await search_repository.create(mes.id, mes_without_id)
    return message


@router.get("/users/synchronizations")
async def synchronizations_Users(repository: UserRepository = Depends(UserRepository.get_instance),
                                 search_repository: UserSearchRepository
                                 = Depends(UserSearchRepository.get_instance)
                                 ) -> list[Users]:
    users = await repository.find_all()
    for user in users:
        u = await search_repository.test_find(user.Id)
        mes_without_id = {key: value for key, value in user.dict().items() if key != 'id'}
        if u:
            await search_repository.update(user.Id, mes_without_id)
        else:
            await search_repository.create(user.Id, mes_without_id)
    return users


@router.get("/message/")
async def get_all_message(repository: MessageRepository = Depends(MessageRepository.get_instance)) -> list[Messages]:
    return await repository.find_all()


@router.get("/message/{message_id}", response_model=Messages)
async def get_by_id(message_id: str,
                    repository: MessageRepository = Depends(MessageRepository.get_instance)) -> Any:
    if not ObjectId.is_valid(message_id):
        return JSONResponse(content={'status': 'BAD_REQUEST'}, status_code=status.HTTP_400_BAD_REQUEST)
    db_mess = await repository.find_mess_by_id(message_id)
    if db_mess is None:
        return JSONResponse(content={'status': 'NOT_FOUND'}, status_code=status.HTTP_404_NOT_FOUND)
    return db_mess


@router.put("/message/{message_id}", response_model=Messages)
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
    await search_repository.update(message_id, message)
    return db_mess
