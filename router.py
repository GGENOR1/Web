from typing import Any

from bson import ObjectId
from fastapi import APIRouter, Depends, status
from fastapi.openapi.models import Response

from Message_Search_elastic import MessageSearchRepository
from MessagesRepository import MessageRepository
import MessagesRepository
from MessangeClass import Messages, UpdateMessagesModel
from UserRepository import UserRepository
from User_Search_elastic import UserSearchRepository
from UserClass import Users, UpdateUserModel

router = APIRouter()
message: list[Users] = []


# def map_user(user: Any) -> Users:
#     return Users(id=str(user["_id"]),if(creationDate=str(user['CreationDate']))is None)
#
#
# def get_filter(id: str) -> dict:
#     return {'_id': ObjectId(id)}


# вывод всех пользователей
@router.get("/user")
async def get_all_users(repository: UserRepository = Depends(UserRepository.get_instance)) -> list[Users]:
    return await repository.find_all()




# приск по имени
@router.get("/user/search")
async def get_all_users(name: str, repository: UserSearchRepository = Depends(UserSearchRepository.get_instance)) -> \
list[Users]:
    return await repository.get_by_name(name)
@router.get("/message/search/body")
async def get_string(string: str, repository: MessageSearchRepository = Depends(MessageSearchRepository.get_instance)) -> \
list[Messages]:
    return await repository.get_by_Body(string)

@router.get("/message/search/datecreated")
async def get_string(string: str, repository: MessageSearchRepository = Depends(MessageSearchRepository.get_instance)) -> \
list[Messages]:
    return await repository.get_by_date(string)

# поиск по id пользоватлей
@router.get("/user/{user_id}", response_model=Users)
async def get_by_id(user_id: str, repository: UserRepository = Depends(UserRepository.get_instance)) -> Any:
    if not ObjectId.is_valid(user_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    db_user = await repository.get_user_by_id(user_id)
    if db_user is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return db_user

# добавление поользователя
@router.post("/user")
async def add_user(user: UpdateUserModel,
                   repository: UserRepository = Depends(UserRepository.get_instance),
                   search_repository: UserSearchRepository = Depends(UserSearchRepository.get_instance)) -> str:
    user_id = await repository.create(user)
    await search_repository.create(user_id, user)
    return user_id
@router.post("/message")
async def add_messages( message: UpdateMessagesModel,
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
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    db_user = await repository.update(user_id, user)
    if db_user is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    await search_repository.update(user_id, user)
    return db_user

##функция для синхронизации данных из mongodb в ES
@router.get("/message/synchronization")
async def synchronization_Data(repository: MessageRepository = Depends(MessageRepository.get_instance),
                        search_repository: MessageSearchRepository
                        = Depends(MessageSearchRepository.get_instance)
                          ) -> list[Messages]:
    message = await repository.find_all()
    for mes in message:
        post = await search_repository.test_find(mes.id)
        if post:
            await search_repository.update(mes.id, mes)
        else:
            await search_repository.create(mes.id, mes)
    return message

@router.get("/message/")
async def get_all_message(repository: MessageRepository = Depends(MessageRepository.get_instance)) -> list[Messages]:
    return await repository.find_all()


@router.get("/message/{message_id}", response_model=Messages)
async def get_by_id(message_id: str,
                    repository: MessageRepository = Depends(MessageRepository.get_instance)) -> Any:
    if not ObjectId.is_valid(message_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    db_mess = await repository.find_mess_by_id(message_id)
    if db_mess is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return db_mess





@router.put("/message/{message_id}", response_model=Messages)
async def update_messages(message_id: str,
                          message: UpdateMessagesModel,
                          repository: MessageRepository = Depends(MessageRepository.get_instance),
                          search_repository: MessageSearchRepository = Depends(MessageSearchRepository.get_instance)
                          ) -> Any:
    if not ObjectId.is_valid(message_id):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    db_mess = await repository.update_post(message_id, message)
    if db_mess is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    await search_repository.update(message_id, message)
    return db_mess
