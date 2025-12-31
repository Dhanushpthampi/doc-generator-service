from pydantic import BaseModel

class ProposalRequest(BaseModel):
    client_name: str
    discovery: list[str]
    solutions: list[str]
    timeline: list[dict]
    pricing: list[list[str]]
    addons: list[dict]
