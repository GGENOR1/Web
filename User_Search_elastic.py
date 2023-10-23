from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from elasticsearch_utils import get_elasticsearch_client
from massenges import Users


class UserSearchRepository:
    _elasticsearch_client: AsyncElasticsearch
    _elasticsearch_index: str

    def __init__(self, elasticsearch_index: str, elasticsearch_client: AsyncElasticsearch):
        self._elasticsearch_index = elasticsearch_index
        self._elasticsearch_client = elasticsearch_client

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
        user1 = list(map(lambda user: Users(id=user['_id'], creationDate=user['_source']['CreationDate']), hits) )
        return user1

    @staticmethod
    def get_instance(elasticsearch_client: AsyncElasticsearch = Depends(get_elasticsearch_client)):
        elasticsearch_index = "users"
        return UserSearchRepository(elasticsearch_index, elasticsearch_client)
