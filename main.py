import pymongo
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient

from router import router
from DBConnection import close_connect, connect_and_init_db

app = FastAPI()
# url = "mongodb://localhost:27017"
# client = MongoClient(url)

app.include_router(router, tags=["Message"], prefix="/message")
app.add_event_handler("startup", connect_and_init_db )
app.add_event_handler("shutdown", close_connect )




# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}!"}


if __name__ == "__main__":
    uvicorn.run(app, host = '0.0.0.0', port = 8000)

print("hellow world")