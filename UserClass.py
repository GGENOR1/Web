from pydantic import BaseModel


class Users(BaseModel):
    id: str
    Reputation: str
    DisplayName: str
    CreationDate: str
    LastAccessDate:str
    Location:str
    AboutMe:str
    # accountId: str


class UpdateUserModel(BaseModel):
    Reputation: str
    DisplayName: str
    CreationDate: str
    LastAccessDate:str
    Location:str
    AboutMe:str



