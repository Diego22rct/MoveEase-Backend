import json
from pydantic import BaseModel


class IncidentResource(BaseModel):
    title: str
    description: str
    status: str


class Incident(BaseModel):
    id: int
    title: str
    description: str
    status: str
    created_at: str
    updated_at: str

    @classmethod
    def model_load(cls, json_data):
        return cls(**json.loads(json_data))
