from fastapi import FastAPI
from app.routes import example_route

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI + Redis project!"}


app.include_router(example_route.router, prefix="/example", tags=["example"])
