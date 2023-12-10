from pydantic import BaseModel


class Users(BaseModel):
    id: str
    Reputation: int
    CreationDate: str
    DisplayName: str
    LastAccessDate:str
    WebsiteUrl: str
    Location:str
    AboutMe:str
    Views:int
    UpVotes:int
    DownVotes:int
    AccountId:str
    # accountId: str


class UpdateUserModel(BaseModel):
    Reputation: int
    CreationDate: str
    DisplayName: str
    LastAccessDate:str
    WebsiteUrl: str
    Location:str
    AboutMe:str
    Views:int
    UpVotes:int
    DownVotes:int
    AccountId:str


