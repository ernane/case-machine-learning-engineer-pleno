from typing import Dict, List

from fastapi import APIRouter

from src.adapters.repositories.prediction_repository.mongomock_repository import (  # noqa: E501
    InMemoryPredictionRepository,
)

# Criar o roteador para o histórico
router = APIRouter()

# Instanciar o repositório de predições
prediction_repository = InMemoryPredictionRepository()


@router.get('/model/history/', response_model=Dict[str, List[Dict]])
async def get_prediction_history() -> Dict[str, List[Dict]]:
    """
    Exibe o histórico das predições realizadas.
    """
    history = (
        await prediction_repository.get_all_predictions()
    )  # Usar o repositório
    return {'history': history}
