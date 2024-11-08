from fastapi import APIRouter
from app.domain.model.Incident import IncidentResource
from app.domain.IncidentServices import IncidentsService

router = APIRouter()
service = IncidentsService()


@router.post("/incidents")
def create_incident(data: IncidentResource):
    try:
        print("Data received:", data)
        return service.save_data(data)
    except Exception as e:
        return {"error": str(e)}


@router.delete("/incidents/{key}")
def delete_incident(key: str):
    try:
        return service.delete_data(key)
    except Exception as e:
        return {"error": str(e)}


@router.put("/incidents/{key}")
def update_incident(key: str, data: IncidentResource):
    try:
        return service.update_data(key, data)
    except Exception as e:
        return {"error in put": str(e)}


@router.get("/incidents/{key}")
def read_incident(key: str):
    try:
        return service.get_data(key)
    except Exception as e:
        return {"error": str(e)}


@router.get("/incidents/")
def read_all_incidents():
    try:
        return service.get_all_data()
    except Exception as e:
        return {"error": str(e)}
