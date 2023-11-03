from pydantic import BaseModel


class Messages(BaseModel):
    id: str
    PostTypeId: int
    AcceptedAnswerId: int
    CreationDate: str
    Score: int
    ViewCount: int
    Body: str
    OwnerUserId: int
    LastActivityDate: str
    Title: str
    Tags: str
    AnswerCount: int
    CommentCount: int
    ContentLicense: str
    LastEditorUserId: int
    LastEditDate: str


class UpdateMessagesModel(BaseModel):
    PostTypeId: int
    AcceptedAnswerId: int
    CreationDate: str
    Score: int
    ViewCount: int
    Body: str
    OwnerUserId: int
    LastActivityDate: str
    Title: str
    Tags: str
    AnswerCount: int
    CommentCount: int
    ContentLicense: str
    LastEditorUserId: int
    LastEditDate: str
