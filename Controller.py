from DBConnection import connect_and_init_db, close_connect
from elasticsearch_utils import connect_elasticsearch_and_init, close_connect_ES


async def handle_startup():
    await connect_elasticsearch_and_init()
    await connect_and_init_db()


async def handle_shutdown():
    await close_connect()
    await close_connect_ES()