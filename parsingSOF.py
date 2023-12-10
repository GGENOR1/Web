import codecs
import xml.etree.ElementTree as ET
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["USER2"]

collection = db["User"]

tree = ET.parse("DUMB/Users.xml")
root = tree.getroot()

# Проход по элементам XML и запись в MongoDB
for row in root.findall('row'):
    user_data = {

        'Reputation': int(row.get('Reputation',0)),
        'CreationDate': row.get('CreationDate',"0000-00-00"),
        'DisplayName': codecs.encode(row.get('DisplayName', ""), 'utf-8', 'ignore').decode('utf-8'),
        'LastAccessDate': row.get('LastAccessDate',"0000-00-00"),
        'WebsiteUrl': codecs.encode(row.get('WebsiteUrl', ""), 'utf-8', 'ignore').decode('utf-8'),
        'Location': row.get('Location',""),
        'AboutMe': codecs.encode(row.get('AboutMe', ""), 'utf-8', 'ignore').decode('utf-8'),
        'Views': int(row.get('Views',0)),
        'UpVotes': int(row.get('UpVotes',0)),
        'DownVotes': int(row.get('DownVotes',0)),
        'AccountId': row.get('AccountId',"-1"),
    }

    collection.insert_one(user_data)
print(user_data)
client.close()


# client = MongoClient("mongodb://localhost:27017/")
#
# db = client["USER2"]
#
# collection = db["Message"]
#
# tree = ET.parse("DUMB/Posts.xml")
# root = tree.getroot()
#
# # Проход по элементам XML и запись в MongoDB
# for row in root.findall('row'):
#     mes_data = {
#         'PostTypeId': int(row.get('PostTypeId',0)),
#         'AcceptedAnswerId': int(row.get('AcceptedAnswerId', 0)),
#         'CreationDate': row.get('CreationDate',"1000-01-01"),
#         "Score": int(row.get('Score', 0)),
#         "ViewCount": int(row.get('ViewCount', 0)),
#         'Body': row.get('Body', ""),
#         "OwnerUserId": int(row.get('OwnerUserId', 0)),
#         'LastActivityDate': row.get('LastActivityDate',"1000-01-01"),
#         'Title': row.get('Title', ""),
#         'Tags': row.get('Tags', ""),
#         "AnswerCount": int(row.get('AnswerCount', 0)),
#         "CommentCount": int(row.get('CommentCount', 0)),
#         'ContentLicense': row.get('ContentLicense', ""),
#         "LastEditorUserId": int(row.get('LastEditorUserId', 0)),
#         'LastEditDate': row.get('LastEditDate', "1000-01-01"),
#
#     }
#
#     collection.insert_one(mes_data)
# print(mes_data)
# client.close()
# #
# def insert_data_into_mongodb(data):
#     collection.insert_many(data)
#
#

#
# data = get_stackoverflow_data(tag)
# print(data)
# insert_data_into_mongodb(data)
