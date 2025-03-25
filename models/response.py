from pydantic import BaseModel
from typing import Optional

class ChatResponse(BaseModel):
    answer: str
    source_agent: Optional[str] = None 