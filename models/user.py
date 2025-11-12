from pydantic import BaseModel, EmailStr

from bson import ObjectId
from models.url import CodeInput


class UserDoc(BaseModel):

    _id: ObjectId
    email: EmailStr
    hashed_password: str
    linked_urls: list[CodeInput]


class GetUserRequest(BaseModel):

    _id: ObjectId
