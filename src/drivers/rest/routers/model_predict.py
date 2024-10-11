from typing import List

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from src.adapters.repositories.model_repository.disk_repository import (
    DiskModelRepository,
)
from src.adapters.repositories.prediction_repository.mongomock_repository import (  # noqa: E501
    InMemoryPredictionRepository,
)
from src.models.model_definitions import DummyModel
from src.use_cases.model_predict_use_case import ModelPredictUseCase

dummy_model = DummyModel()
router = APIRouter()

# Criar o repositório e o caso de uso de predição
repository = DiskModelRepository()
predict_use_case = ModelPredictUseCase(model_repository=repository)
prediction_repository = InMemoryPredictionRepository()


class PredictionInput(BaseModel):
    input_data: List[List[float]]


@router.post('/model/predict/')
async def predict(input: PredictionInput):
    try:
        await predict_use_case.load_model('/tmp/model.pkl')

        predictions = await predict_use_case(input.input_data)

        prediction_entry = {
            'input': input.input_data,
            'predicted': predictions.tolist()
            if hasattr(predictions, 'tolist')
            else predictions,
        }
        await prediction_repository.add_prediction(prediction_entry)

        return {
            'predictions': predictions.tolist()
            if hasattr(predictions, 'tolist')
            else predictions
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Error making prediction: {str(e)}',
        )
