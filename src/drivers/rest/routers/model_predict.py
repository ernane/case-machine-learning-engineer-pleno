from typing import List

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from src.adapters.repositories.model_repository.disk_repository import (
    DiskModelRepository,
)
from src.use_cases.model_predict_use_case import ModelPredictUseCase

router = APIRouter()

# Criar o repositório e o caso de uso de predição
repository = DiskModelRepository()
predict_use_case = ModelPredictUseCase(model_repository=repository)


class DummyModel:
    def predict(self, X):
        return [len(x) for x in X]


class PredictionInput(BaseModel):
    input_data: List[List[int]]


@router.post('/model/predict/')
async def predict(input: PredictionInput):
    try:
        await predict_use_case.load_model('/tmp/model.pkl')

        # Chama o caso de uso de predição
        predictions = await predict_use_case(input.input_data)
        return {'predictions': predictions}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Error making prediction: {str(e)}',
        )
