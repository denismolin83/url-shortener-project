from typing_extensions import Self
from pydantic import BaseModel, ConfigDict, AnyHttpUrl, field_validator, Field
from datetime import datetime
import re


class URLCreate(BaseModel):
    target_url: AnyHttpUrl = Field(..., max_length=2000)

    @field_validator('target_url')
    @classmethod
    def validate_url_content(cls, v: AnyHttpUrl):
        url_str = str(v)

        if "my-shortener-doman.ru" in url_str:
            raise ValueError("Нельзя сокращать ссылки на этот же сервер")
        
        return v



class URLInfo(BaseModel):
    id: int
    short_key: str
    original_url: str
    created_at: datetime
    hits: int

    model_config= ConfigDict(from_attributes=True)