from pydantic import BaseModel


class Messages(BaseModel):
    id: str
    PostTypeId: str
    AcceptedAnswerId: str
    CreationDate: str
    Score: str
    ViewCount: str
    Body: str
    OwnerUserId: str
    LastActivityDate: str
    Title: str
    Tags: str
    AnswerCount: str
    CommentCount: str
    ContentLicense: str
    LastEditorUserId: str
    LastEditDate: str


class UpdateMessagesModel(BaseModel):
    CreationDate: str
    Body: str
    Title: str
    Tags: str
    LastEditDate: str
