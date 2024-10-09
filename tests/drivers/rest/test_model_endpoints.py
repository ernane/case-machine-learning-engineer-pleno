from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import status
from httpx import AsyncClient

from src.adapters.repositories.model_repository.disk_repository import (
    DiskModelRepository,
)
from src.drivers.rest.main import app
from src.use_cases.model_load_use_case import ModelLoadUseCase


@pytest.fixture
def mock_repository():
    return MagicMock(spec=DiskModelRepository)


@pytest.fixture
def model_loader(mock_repository):
    return ModelLoadUseCase(model_repository=mock_repository)


@pytest.mark.asyncio
async def test_load_model_success(monkeypatch):
    # Mocking the repository and use case
    mock_model_loader = MagicMock()

    mock_model_loader.return_value = {
        'status': 'success',
        'message': 'Model loaded successfully',
        'path': '/home/ejjunior/Downloads/model.pkl',
    }

    # Patching the use case inside the endpoint
    with patch(
        'src.use_cases.model_load_use_case.ModelLoadUseCase',
        return_value=mock_model_loader,
    ):
        async with AsyncClient(app=app, base_url='http://test') as ac:
            files = {'file': ('model.pkl', b'dummy content')}
            response = await ac.post('/model/load/', files=files)

        # Verifying the response
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            'status': 'success',
            'message': 'Model loaded successfully',
            'path': '/tmp/model.pkl',
        }


@pytest.mark.asyncio
async def test_load_model_invalid_extension():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        files = {'file': ('model.txt', b'dummy content')}
        response = await ac.post('/model/load/', files=files)

    # Verifying the response
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Only .pkl files are supported'}


@pytest.mark.asyncio
async def test_load_model_internal_server_error():
    # Simula um erro ao carregar o modelo com AsyncMock
    mock_model_loader = AsyncMock(
        side_effect=Exception('Failed to load model')
    )

    # Patch no ponto correto: __call__ do ModelLoadUseCase
    with patch(
        'src.use_cases.model_load_use_case.ModelLoadUseCase.__call__',
        mock_model_loader,
    ):
        async with AsyncClient(app=app, base_url='http://test') as ac:
            files = {'file': ('model.pkl', b'dummy content')}
            response = await ac.post('/model/load/', files=files)

    # Verifica se o código de status retornado é 500
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert 'Error loading model' in response.json()['detail']
