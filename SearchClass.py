from MessangeClass import Messages


class MessageParams:
    @staticmethod
    def convert(mess):
        return Messages(id=mess['_id'],
                        PostTypeId=mess['_source'].get('PostTypeId', "None"),
                        AcceptedAnswerId=mess['_source'].get('AcceptedAnswerId', "None"),
                        CreationDate=mess['_source'].get('CreationDate', "None"),
                        Score=mess['_source'].get('Score', "None"),
                        ViewCount=mess['_source'].get('ViewCount', "None"),
                        Body=mess['_source'].get('Body', "None"),
                        OwnerUserId=mess['_source'].get('OwnerUserId', "None"),
                        LastActivityDate=mess['_source'].get('LastActivityDate', "None"),
                        Title=mess['_source'].get('Title', "None"),
                        Tags=mess['_source'].get('Tags', "None"),
                        AnswerCount=mess['_source'].get('AnswerCount', "None"),
                        CommentCount=mess['_source'].get('CommentCount', "None"),
                        ContentLicense=mess['_source'].get('ContentLicense', "None"),
                        LastEditorUserId=mess['_source'].get('LastEditorUserId', "None"),
                        LastEditDate=mess['_source'].get('LastEditDate', "None"))
