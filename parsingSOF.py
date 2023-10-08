import requests
import xml.etree.ElementTree as ET
from pymongo import MongoClient







# def get_stackoverflow_data(tag):
#     url = f"https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&tagged={tag}&site=stackoverflow"
#     response = requests.get(url)
#     data = response.json()['items']
#
#     return data


# Установка соединения с MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Выбор базы данных
db = client["your_database2"]

# Выбор коллекции
collection = db["your_collection2"]


# Parse and insert XML data into MongoDB
tree = ET.parse("DUMB/Users.xml")  # Path to your XML file
root = tree.getroot()

for row in root.findall('row'):
    emp_react = {}
    for attribute, value in row.items():
        emp_react[attribute] = value
    collection.insert_one(emp_react)


print(emp_react)
# Close MongoDB connection
client.close()


#
# def insert_data_into_mongodb(data):
#     collection.insert_many(data)
#
#
# tag = "python"  # задайте тэг, по которому хотите получить данные
#
# data = get_stackoverflow_data(tag)
# print(data)
# insert_data_into_mongodb(data)