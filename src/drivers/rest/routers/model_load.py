from fastapi import APIRouter, File, HTTPException, UploadFile, status

from src.adapters.repositories.model_repository.disk_repository import (
    DiskModelRepository,
)
from src.models.model_definitions import DummyModel
from src.use_cases.model_load_use_case import ModelLoadUseCase

dummy_model = DummyModel()
router = APIRouter()

# Cria o repositório e caso de uso
repository = DiskModelRepository()
model_loader = ModelLoadUseCase(model_repository=repository)


@router.post('/model/load/')
async def load_model(file: UploadFile = File(...)):
    if not file.filename.endswith('.pkl'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Only .pkl files are supported',
        )
    try:
        model_data = await file.read()
        result = await model_loader(model_data, '/tmp/model.pkl')
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Error loading model: {str(e)}',
        )
