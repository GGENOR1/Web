import pymongo
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient

from Controller import handle_startup, handle_shutdown
from router import router
from DBConnection import close_connect, connect_and_init_db

app = FastAPI()
# url = "mongodb://localhost:27017"
# client = MongoClient(url)

app.include_router(router, tags=["Message"], prefix="/user")
app.add_event_handler("startup", handle_startup )
app.add_event_handler("shutdown", handle_shutdown )

if __name__ == "__main__":
    uvicorn.run(app, host = '0.0.0.0', port = 8000)

print("hellow world")