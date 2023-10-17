from pydantic import BaseModel


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