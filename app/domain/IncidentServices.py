from datetime import datetime
import json
from app.core.infrastructure.redis_client import get_redis_client
from app.domain.model.Incident import Incident, IncidentResource


class IncidentsService:
    def __init__(self):
        self.client = get_redis_client()
        self.incident_counter_key = "incidents_counter"

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
            self.client.json().set(f"incidents:{incident_id}", "$", serialized_data)
            return incident_to_save
        except Exception as e:
            self.client.decr(self.incident_counter_key)
            return {"error in IncidentsService": str(e)}

    def delete_data(self, incident_id: int):
        try:
            key = f"incidents:{incident_id}"
            result = self.client.delete(key)
            if result == 1:
                return {"message": f"Incident with ID {incident_id} deleted"}
            return {"message": "Incident not found"}
        except Exception as e:
            return {"error": str(e)}

    def update_data(self, key: str, data: IncidentResource):
        saved_incident_json = self.get_data(key)
        if not saved_incident_json:
            return {"error": "Incident not found"}
        try:
            self.client.json().set(f"incidents:{key}", "$.title", data.title)
            self.client.json().set(
                f"incidents:{key}", "$.description", data.description
            )
            self.client.json().set(f"incidents:{key}", "$.status", data.status)
            self.client.json().set(
                f"incidents:{key}",
                "$.updated_at",
                datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),
            )
            return {
                "message": f"Incident with ID {key} updated",
                "data": Incident(
                    id=int(key),
                    title=data.title,
                    description=data.description,
                    status=data.status,
                    created_at=saved_incident_json.get("created_at"),
                    updated_at=datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),
                ),
            }
        except Exception as e:
            return {"error in update": str(e)}

    def get_data(self, key: str):
        try:
            data = self.client.json().get(f"incidents:{key}")
            return data
        except Exception as e:
            return {"error": str(e)}

    def get_all_data(self):
        try:
            keys = self.client.keys("incidents:*")
            data = [self.client.json().get(key) for key in keys]
            return data
        except Exception as e:
            return {"error": str(e)}
