from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from MessangeClass import UpdateMessagesModel
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

    async def delete(self, mess_id: str):
        await (self._elasticsearch_client.delete(index=self._elasticsearch_index, id=mess_id))

    @staticmethod
    def get_instance(elasticsearch_client: AsyncElasticsearch = Depends(get_elasticsearch_client)):
        elasticsearch_index = "messages"
        return MessageSearchRepository(elasticsearch_index, elasticsearch_client)
