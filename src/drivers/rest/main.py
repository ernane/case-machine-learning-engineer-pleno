from fastapi import FastAPI

from src.drivers.rest.routers import (
    health,
    model_history,
    model_load,
    model_predict,
)

app = FastAPI()

app.include_router(health.router)
app.include_router(model_load.router)
app.include_router(model_predict.router)
app.include_router(model_history.router)
