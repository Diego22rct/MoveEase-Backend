from fastapi import FastAPI
from app.routes import incidentsRoute

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI + Redis project!"}


app.include_router(incidentsRoute.router, tags=["Incidents"], prefix="/api/v1")
