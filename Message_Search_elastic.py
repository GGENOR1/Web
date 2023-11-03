from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from MessangeClass import UpdateMessagesModel, Messages
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

        # query = {
        #     "match": {
        #         "Body": {
        #             "query": String,
        #             "minimum_should_match": "50%"
        #         }
        #     }
        # }
        # {
        #     "query": {
        #         "match": {
        #             "Body": {"query": "afaf"}
        #         }
        #     }
        # }
        response = await self._elasticsearch_client.search(index=self._elasticsearch_index, query=query,
                                                           filter_path=["hits.hits._id", "hits.hits._source"])
        hits = response.body['hits']['hits']
        message = list(map(lambda mess: Messages(
            id=mess['_id'],
            PostTypeId=mess['_source'].get('PostTypeId', "None"),
            AcceptedAnswerId=mess['_source'].get('AcceptedAnswerId', "None"),
            CreationDate=mess['_source'].get('CreationDate',  "None"),
            Score=mess['_source'].get('Score', "None"),
            ViewCount=mess['_source'].get('ViewCount', "None"),
            Body=mess['_source'].get('Body', "None"),
            OwnerUserId = mess['_source'].get('OwnerUserId', "None"),
            LastActivityDate = mess['_source'].get('LastActivityDate', "None"),
            Title = mess['_source'].get('Title', "None"),
            Tags = mess['_source'].get('Tags', "None"),
            AnswerCount = mess['_source'].get('AnswerCount', "None"),
            CommentCount = mess['_source'].get('CommentCount', "None"),
            ContentLicense=mess['_source'].get('ContentLicense', "None"),
            LastEditorUserId=mess['_source'].get('LastEditorUserId', "None"),
            LastEditDate=mess['_source'].get('LastEditDate', "None")),hits))
        return message

    async def get_by_date(self, date: str) -> list[Messages]:
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

        # query = {
        #     "match": {
        #         "Body": {
        #             "query": String,
        #             "minimum_should_match": "50%"
        #         }
        #     }
        # }
        # {
        #     "query": {
        #         "match": {
        #             "Body": {"query": "afaf"}
        #         }
        #     }
        # }
        response = await self._elasticsearch_client.search(index=self._elasticsearch_index, query=query,
                                                           filter_path=["hits.hits._id", "hits.hits._source"])
        hits = response.body['hits']['hits']
        message = list(map(lambda mess: Messages(
            id=mess['_id'],
            PostTypeId=mess['_source'].get('PostTypeId', "None"),
            AcceptedAnswerId=mess['_source'].get('AcceptedAnswerId', "None"),
            CreationDate=mess['_source'].get('CreationDate',  "None"),
            Score=mess['_source'].get('Score', "None"),
            ViewCount=mess['_source'].get('ViewCount', "None"),
            Body=mess['_source'].get('Body', "None"),
            OwnerUserId = mess['_source'].get('OwnerUserId', "None"),
            LastActivityDate = mess['_source'].get('LastActivityDate', "None"),
            Title = mess['_source'].get('Title', "None"),
            Tags = mess['_source'].get('Tags', "None"),
            AnswerCount = mess['_source'].get('AnswerCount', "None"),
            CommentCount = mess['_source'].get('CommentCount', "None"),
            ContentLicense=mess['_source'].get('ContentLicense', "None"),
            LastEditorUserId=mess['_source'].get('LastEditorUserId', "None"),
            LastEditDate=mess['_source'].get('LastEditDate', "None")),hits))
        return message


    @staticmethod
    def get_instance(elasticsearch_client: AsyncElasticsearch = Depends(get_elasticsearch_client)):
        elasticsearch_index = "messages"
        return MessageSearchRepository(elasticsearch_index, elasticsearch_client)
