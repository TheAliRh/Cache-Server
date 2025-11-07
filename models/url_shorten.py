"""This module is used for shortener urls models"""

from pydantic import BaseModel, AnyHttpUrl, Field
from typing import Optional
from datetime import datetime


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

    _id: Optional[str]
    code: str
    original_url: str
    created_at: datetime
    expires_in_seconds: Optional[datetime]
    clicks: int = 0
