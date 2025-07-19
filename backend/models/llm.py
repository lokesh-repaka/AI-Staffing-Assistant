from pydantic import BaseModel
from typing import Optional

class LLMQuery(BaseModel):
    query: Optional[str] = None
    file_path: Optional[str] = None

class LLMResponse(BaseModel):
    response: str