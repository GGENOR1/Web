from elasticsearch import AsyncElasticsearch

elasticsearch_client: AsyncElasticsearch = None


async def connect_elasticsearch_and_init():
    global elasticsearch_client
    elasticsearch_url = "http://localhost:9200"
    try:
        elasticsearch_client = AsyncElasticsearch(elasticsearch_url)
        await elasticsearch_client.info()
        print(f"Connection to ES with {elasticsearch_url}")

    except Exception as Ex:
        print(f"Cant connect to ES: {Ex}")


async def close_connect_ES():
    if elasticsearch_client is None:
        return
    await elasticsearch_client.close()


def get_elasticsearch_client():
    return elasticsearch_client
