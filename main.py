import pymongo
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI()
url = "mongodb://localhost:27017"
client = MongoClient(url)

class Message(BaseModel):
    id: str
    text: str

# Класс-сервис для работы с MongoDB
class MessageService:
    def __init__(self, client, database_name, collection_name):
        self.client = client
        self.database = self.client[database_name]
        self.collection = self.database[collection_name]

    def save_message(self, message: Message):
        self.collection.insert_one(message.dict())

    def find_message(self, id: str) -> Message:
        mess = self.collection.find_one({"id": id})
        print(mess)
        print()
        if mess:
            return mess["text"]
        else:
             return ("error find")

# Создаем экземпляр класса-сервиса MongoDB
message_service = MessageService(client, "test", "testuser")

# Маршрут для сохранения сообщения
@app.post("/api/messages")
def create_message(message: Message):
    message_service.save_message(message)
    return {"message": "Message saved"}

@app.get("/api/messages/{id}")
def find_create_message(id: str):
    return {message_service.find_message(id)}
print("hellow")

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
