from pydantic import BaseModel, EmailStr

from bson import ObjectId
from models.url import CodeInput


class UserDoc(BaseModel):

    _id: ObjectId
    email: EmailStr
    password: str
    linked_urls: list[CodeInput]
