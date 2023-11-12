from elasticsearch import AsyncElasticsearch

from fastapi import Depends, status
from starlette.responses import JSONResponse

from Models.MessangeClass import UpdateMessagesModel, Messages
from SearchClass import MessageParams
from elasticsearch_utils import get_elasticsearch_client




class MessageSearchRepository:
    _elasticsearch_client: AsyncElasticsearch
    _elasticsearch_index: str

    def __init__(self, elasticsearch_index: str, elasticsearch_client: AsyncElasticsearch):
        self._elasticsearch_index = elasticsearch_index
        self._elasticsearch_client = elasticsearch_client

    async def create(self, mess_id: str, mess: UpdateMessagesModel):
        await self._elasticsearch_client.create(index=self._elasticsearch_index, id=mess_id, document=dict(mess))

    async def update(self, mess_id: str, mess: UpdateMessagesModel):
        await self._elasticsearch_client.update(index=self._elasticsearch_index, id=mess_id, doc=dict(mess))

    async def get_by_Body(self, String: str) -> list[Messages]:
        exact_match_query = {
            "match": {
                "Body": String
            }
        }
        fuzzy_match_query = {
            "fuzzy": {
                "Body": {
                    "value": String,
                    "fuzziness": "AUTO"
                }
            }
        }
        query = {
            "bool": {
                "should": [exact_match_query, fuzzy_match_query]
            }
        }

        response = await self._elasticsearch_client.search(index=self._elasticsearch_index, query=query,
                                                           filter_path=["hits.hits._id", "hits.hits._source"])
        if not response: JSONResponse(content = {'status' : 'Not Found'}, status_code=status.HTTP_404_NOT_FOUND)
        hits = response.body['hits']['hits']
        message = list(map(MessageParams.convert, hits))
        return message


    async def delete(self, mess_id: str):
        await (self._elasticsearch_client.delete(index=self._elasticsearch_index, id=mess_id))

    async def test_find(self, mess_id: str):
       ex = await (self._elasticsearch_client.exists(index=self._elasticsearch_index, id=mess_id))
       print(ex)
       if ex:
           print(f"Индекс {mess_id} существует")
       else:
           print(f"Индекс {mess_id} не существует")
       return ex





    async def get_by_date(self, date1:str="2010-01-12", date2:str="now/d") -> list[Messages]:
        query = {
            "range": {
                "CreationDate": {
                    "gte": date1,
                    "lte": date2
                }
            }
        }


        response = await self._elasticsearch_client.search(index=self._elasticsearch_index, query=query,
                                                           filter_path=["hits.hits._id", "hits.hits._source"])
        if not response: return JSONResponse(content = {'status' : 'Not Found'}, status_code=status.HTTP_404_NOT_FOUND)
        hits = response.body['hits']['hits']
        message = list(map(MessageParams.convert, hits))
        return message

    @staticmethod
    def get_instance(elasticsearch_client: AsyncElasticsearch = Depends(get_elasticsearch_client)):
        elasticsearch_index = "messages2"
        return MessageSearchRepository(elasticsearch_index, elasticsearch_client)
