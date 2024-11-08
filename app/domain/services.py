from app.core.infrastructure.redis_client import get_redis_client
from app.domain.models import ExampleData


class ExampleService:
    def __init__(self):
        self.client = get_redis_client()

    def save_data(self, data: ExampleData):
        self.client.set(data.key, data.value)
        return {"message": "Data saved successfully."}

    def get_data(self, key: str):
        value = self.client.get(key)
        if value:
            return {"key": key, "value": value}
        return {"error": "Key not found."}
