# models.py
from typing import Any, Dict

from pydantic import BaseModel, Field


class MyResponse(BaseModel):
    success: bool
    error: str
    message: str
    content: Any


class GETKEY(BaseModel):
    public_key: str


class DotDict:
    def __init__(self, dictionary: Dict[str, Any]):
        self.__dict__ = dictionary
