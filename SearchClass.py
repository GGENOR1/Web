from Models.MessangeClass import Messages
from Models.UserClass import Users


class MessageParams:
    @staticmethod
    def convert(mess):
        return Messages(id=mess['_id'],
                        PostTypeId=mess['_source'].get('PostTypeId', "None"),
                        AcceptedAnswerId=mess['_source'].get('AcceptedAnswerId', "None"),
                        CreationDate=mess['_source'].get('CreationDate', "None"),
                        Score=mess['_source'].get('Score', 0),
                        ViewCount=mess['_source'].get('ViewCount', 0),
                        Body=mess['_source'].get('Body', "None"),
                        OwnerUserId=mess['_source'].get('OwnerUserId', "None"),
                        LastActivityDate=mess['_source'].get('LastActivityDate', "None"),
                        Title=mess['_source'].get('Title', "None"),
                        Tags=mess['_source'].get('Tags', "None"),
                        AnswerCount=mess['_source'].get('AnswerCount', 0),
                        CommentCount=mess['_source'].get('CommentCount', 0),
                        ContentLicense=mess['_source'].get('ContentLicense', 0),
                        LastEditorUserId=mess['_source'].get('LastEditorUserId', "None"),
                        LastEditDate=mess['_source'].get('LastEditDate', "None"))

    @staticmethod
    def convertUser(user):
        return Users(
                        id=user['_id'],
                        Reputation=user['_source'].get('Reputation', 0),
                        CreationDate=user['_source'].get('CreationDate', "None"),
                        DisplayName=user['_source'].get('DisplayName', "None"),
                        LastAccessDate=user['_source'].get('LastAccessDate', "None"),
                        WebsiteUrl=user['_source'].get('WebsiteUrl', "None"),
                        Location=user['_source'].get('Location', "None"),
                        AboutMe=user['_source'].get('AboutMe', "None"),
                        Views=user['_source'].get('Views', 0),
                        UpVotes=user['_source'].get('UpVotes', 0),
                        DownVotes=user['_source'].get('DownVotes', 0),
                        AccountId=user['_source'].get('AccountId', "None"),
                        )
