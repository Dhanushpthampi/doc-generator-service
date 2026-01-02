from pydantic import BaseModel
from typing import Optional, List

class ContractRequest(BaseModel):
    client_name: str
    project_name: str
    scope_of_work: List[str]
    payment_terms: str
    start_date: str
    end_date: Optional[str] = None
    total_amount: str
