from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

class ProposalRequest(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )
    client_name: str
    recommended_services: list[str] = []
    timeline: list[dict]
    pricing: list[list[str]]
