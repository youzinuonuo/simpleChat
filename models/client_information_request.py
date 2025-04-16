from pydantic import BaseModel
from typing import Optional

class ClientInformationRequest(BaseModel):
    """
    Request model for client information lookup.
    Either member_number or client_name must be provided.
    """
    member_number: Optional[str] = None
    client_name: Optional[str] = None
