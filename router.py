from typing import Any

from bson import ObjectId
from fastapi import APIRouter, Depends, status
from fastapi.openapi.models import Response
from UserRepository import UserRepository
from User_Search_elastic import UserSearchRepository
from massenges import Users, UpdateUserModel

router = APIRouter()
message: list[Users] = []


# def map_user(user: Any) -> Users:
#     return Users(id=str(user["_id"]),if(creationDate=str(user['CreationDate']))is None)
#
#
# def get_filter(id: str) -> dict:
#     return {'_id': ObjectId(id)}


# вывод всех пользователей
@router.get("/")
async def get_all_users(repository: UserRepository = Depends(UserRepository.get_instance)) -> list[Users]:
    return await repository.find_all()

@router.get("/search")
async def get_all_users(date: str, repository: UserSearchRepository = Depends(UserSearchRepository.get_instance)) -> list[Users]:
    return await repository.get_by_name(date)



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


