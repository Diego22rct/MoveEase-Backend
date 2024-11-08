from fastapi import APIRouter
from app.domain.models import ExampleData
from app.domain.services import ExampleService

router = APIRouter()
service = ExampleService()


@router.post("/data/")
def create_data(data: ExampleData):
    return service.save_data(data)


@router.get("/data/{key}")
def read_data(key: str):
    return service.get_data(key)
