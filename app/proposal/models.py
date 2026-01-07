from pydantic import BaseModel

class ProposalRequest(BaseModel):
    client_name: str
    recommended_services: list[str] = []
    timeline: list[dict]
    pricing: list[list[str]]
