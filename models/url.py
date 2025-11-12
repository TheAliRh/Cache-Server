"""This module is used for shortener urls models"""

from pydantic import BaseModel, HttpUrl, AnyHttpUrl, Field, validator

from bson import ObjectId
from typing import Optional
from datetime import datetime
import re


class ShortenRequest(BaseModel):
    """This class is used for"""

    original_url: AnyHttpUrl
    custom_code: Optional[str] = None
    expires_in_seconds: Optional[int] = None


class ShortenResponse(BaseModel):
    """This class is used for"""

    code: str
    url: AnyHttpUrl
    original_url: AnyHttpUrl
    expires_in_seconds: Optional[int]


class URLDoc(BaseModel):
    """
    This class is used for keeping status of shortened urls.
    """

    _id: str
    code: str
    original_url: str
    created_at: datetime
    expires_in_seconds: Optional[datetime]
    clicks: int


class URLInput(BaseModel):
    url: HttpUrl


class CodeInput(BaseModel):

    code: str

    @validator("code")
    def validate_code(cls, v):
        """
        Only allow uppercase letters, lowercase letters, and numbers.
        """
        if not re.match(r"^[A-Za-z0-9]+$", v):
            raise ValueError(
                "Code can only contain letters and numbers (A–Z, a–z, 0–9)"
            )
        return v


class URLSummery(BaseModel):

    code: str
    clicks: int


class CreateURLRequest(BaseModel):

    original_url: HttpUrl
    code: CodeInput = None
    expire_time: datetime = None


class UpdateURLRequest(BaseModel):

    current_code: CodeInput
    new_code: CodeInput


class DeleteURLRequest(BaseModel):

    code: CodeInput


class GetURLRequest(BaseModel):

    code: CodeInput
