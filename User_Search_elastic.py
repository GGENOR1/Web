from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from elasticsearch_utils import get_elasticsearch_client
from massenges import Users, UpdateUserModel


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

    async def get_by_name(self, date: str) -> list[Users]:
        query = {
            "match": {
                "CreationDate": {
                    "query": date
                }
            }
        }

        response = await self._elasticsearch_client.search(index=self._elasticsearch_index, query=query,
                                                           filter_path=["hits.hits._id", "hits.hits._source"])
        hits = response.body['hits']['hits']
        user1 = list(map(lambda user: Users(id=user['_id'],Reputation=user['_source']['Reputation'], DisplayName=user['_source']['DisplayName'], CreationDate=user['_source']['CreationDate'], LastAccessDate=user['_source']['LastAccessDate'] ), hits))
        return user1




    @staticmethod
    def get_instance(elasticsearch_client: AsyncElasticsearch = Depends(get_elasticsearch_client)):
        elasticsearch_index = "users"
        return UserSearchRepository(elasticsearch_index, elasticsearch_client)
