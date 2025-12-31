from pydantic import BaseModel, ConfigDict, HttpUrl
from datetime import datetime


class URLCreate(BaseModel):
    target_url: HttpUrl


class URLInfo(BaseModel):
    id: int
    short_key: str
    original_url: str
    created_at: datetime
    hits: int

    model_config= ConfigDict(from_attributes=True)