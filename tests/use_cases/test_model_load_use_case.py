from unittest.mock import AsyncMock, MagicMock

import pytest

from src.use_cases.model_load_use_case import ModelLoadUseCase


@pytest.fixture
def mock_repository():
    repository = MagicMock()
    repository.save = AsyncMock()
    return repository


@pytest.fixture
def model_load_use_case(mock_repository):
    return ModelLoadUseCase(model_repository=mock_repository)


@pytest.mark.asyncio
async def test_model_load_use_case_success(
    model_load_use_case, mock_repository
):
    # Defina dados fictícios do modelo e caminho
    model_data = b'dummy_model_data'
    model_path = 'path/to/model.pkl'

    # Chama o caso de uso
    result = await model_load_use_case(model_data, model_path)

    # Verifica se o repositório salvou o modelo corretamente
    mock_repository.save.assert_called_once_with(model_data, model_path)

    # Verifica o retorno esperado
    assert result == {
        'status': 'success',
        'message': 'Model loaded successfully',
        'path': model_path,
    }


@pytest.mark.asyncio
async def test_model_load_use_case_failure(mock_repository):
    # Simula uma exceção ao salvar o modelo
    mock_repository.save.side_effect = Exception('Save failed')

    model_load_use_case = ModelLoadUseCase(model_repository=mock_repository)

    model_data = b'dummy_model_data'
    model_path = 'path/to/model.pkl'

    # Verifica se a exceção é lançada corretamente
    with pytest.raises(Exception, match='Save failed'):
        await model_load_use_case(model_data, model_path)
