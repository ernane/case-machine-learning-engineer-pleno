from fastapi import FastAPI

from src.drivers.rest.routers import health, model_load

app = FastAPI()

app.include_router(health.router)
app.include_router(model_load.router)
