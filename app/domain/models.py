from pydantic import BaseModel


class ExampleData(BaseModel):
    key: str
    value: str
