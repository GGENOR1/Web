
import xml.etree.ElementTree as ET
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["your_database2"]

collection = db["Mess"]

tree = ET.parse("DUMB/Posts.xml")
root = tree.getroot()

for row in root.findall('row'):
    emp_react = {}
    for attribute, value in row.items():
        emp_react[attribute] = value
    collection.insert_one(emp_react)

print(emp_react)
client.close()

#
# def insert_data_into_mongodb(data):
#     collection.insert_many(data)
#
#

#
# data = get_stackoverflow_data(tag)
# print(data)
# insert_data_into_mongodb(data)
