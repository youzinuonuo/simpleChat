from pydantic import BaseModel
from typing import Optional, List

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None
    context: Optional[List[str]] = None 