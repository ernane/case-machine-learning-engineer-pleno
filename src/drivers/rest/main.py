from fastapi import FastAPI

from src.drivers.rest.routers import health

app = FastAPI()

app.include_router(health.router)
