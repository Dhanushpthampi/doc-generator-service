from pydantic import BaseModel
from typing import Optional

class NdaRequest(BaseModel):
    client_name: str
    counterparty_name: str
    effective_date: str
    jurisdiction: Optional[str] = "State of California"
