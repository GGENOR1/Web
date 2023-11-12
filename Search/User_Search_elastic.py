from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from SearchClass import MessageParams
from elasticsearch_utils import get_elasticsearch_client
from Models.UserClass import Users, UpdateUserModel


class UserSearchRepository:
    _elasticsearch_client: AsyncElasticsearch
    _elasticsearch_index: str

    def __init__(self, elasticsearch_index: str, elasticsearch_client: AsyncElasticsearch):
        self._elasticsearch_index = elasticsearch_index
        self._elasticsearch_client = elasticsearch_client

    async def create(self, user_id: str, user: UpdateUserModel):
        await self._elasticsearch_client.create(index=self._elasticsearch_index, id=user_id, document=dict(user))

    async def update(self, user_id: str, user: UpdateUserModel):
        await self._elasticsearch_client.update(index=self._elasticsearch_index, id=user_id, doc=dict(user))

    async def delete(self, user_id: str):
        await (self._elasticsearch_client.delete(index=self._elasticsearch_index, id=user_id))
    async def test_find(self, user_id: str):
       ex = await (self._elasticsearch_client.exists(index=self._elasticsearch_index, id=user_id))
       print(ex)
       if ex:
           print(f"Индекс {user_id} существует")
       else:
           print(f"Индекс {user_id} не существует")
       return ex
    async def get_by_name(self, DisplayName: str) -> list[Users]:
        query = {
            "match": {
                "DisplayName": {
                    "query": DisplayName
                }
            }
        }

        response = await self._elasticsearch_client.search(index=self._elasticsearch_index, query=query,
                                                           filter_path=["hits.hits._id", "hits.hits._source"])
        hits = response.body['hits']['hits']
        user1 =list(map(MessageParams.convertUser, hits))
        return user1

    @staticmethod
    def get_instance(elasticsearch_client: AsyncElasticsearch = Depends(get_elasticsearch_client)):
        elasticsearch_index = "users2"
        return UserSearchRepository(elasticsearch_index, elasticsearch_client)
