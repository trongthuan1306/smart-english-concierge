from pydantic import BaseModel
from typing import Any, Optional

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    status: str
    message: str
    skill: Optional[str] = None
    data: Optional[Any] = None

class VocabResponse(BaseModel):
    status: str
    words: list[dict[str, Any]]
