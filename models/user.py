from pydantic import BaseModel, EmailStr

from bson import ObjectId


class UserDoc(BaseModel):

    _id: ObjectId
    email: EmailStr
    password: str
