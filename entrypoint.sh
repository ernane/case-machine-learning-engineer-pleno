#!/bin/sh

# Define a porta padrão como 8000 se ML_API_PORT não estiver definida
PORT=${ML_API_PORT:-8000}

# Inicia o aplicativo FastAPI usando Poetry e Uvicorn
exec poetry run uvicorn --host 0.0.0.0 --port $PORT src.drivers.rest.main:app
