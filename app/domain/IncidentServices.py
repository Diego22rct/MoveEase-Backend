from datetime import datetime
from app.core.infrastructure.redis_client import get_redis_client
from app.domain.model.Incident import Incident, IncidentResource


class IncidentsService:
    def __init__(self):
        self.client = get_redis_client()
        self.incident_counter_key = "incident_counter"

    def save_data(self, data: IncidentResource):
        try:
            incident_id = self.client.incr(self.incident_counter_key)

            incident_to_save = Incident(
                id=incident_id,
                title=data.title,
                description=data.description,
                status=data.status,
                created_at=datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),
                updated_at=datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),
            )

            serialized_data = incident_to_save.model_dump()
            self.client.set(name=f"incident:{incident_id}", value=serialized_data)
            return incident_to_save
        except Exception as e:
            return {"error": str(e)}

    def delete_data(self, incident_id: int):
        try:
            key = f"incident:{incident_id}"
            result = self.client.delete(key)
            if result == 1:
                return {"message": f"Incident with ID {incident_id} deleted"}
            return {"message": "Incident not found"}
        except Exception as e:
            return {"error": str(e)}

    def update_data(self, key: str, data: IncidentResource):
        saved_incident_json = self.get_data(key)
        saved_incident = Incident.model_load(saved_incident_json)
        saved_incident.title = data.title
        saved_incident.description = data.description
        saved_incident.status = data.status
        saved_incident.updated_at = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        serialized_data = saved_incident.model_dump()
        print("Serialized data:", serialized_data)
        try:
            self.client.set(name=f"incident:{key}", value=serialized_data)
            return saved_incident
        except Exception as e:
            return {"error in update": str(e)}

    def get_data(self, key: str):
        try:
            data = self.client.get(f"incident:{key}")
            return data
        except Exception as e:
            return {"error": str(e)}

    def get_all_data(self):
        try:
            keys = self.client.keys("incident:*")
            data = [self.client.get(key) for key in keys]
            return data
        except Exception as e:
            return {"error": str(e)}
