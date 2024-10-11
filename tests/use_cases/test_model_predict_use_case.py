from unittest.mock import AsyncMock, MagicMock

import pytest

from src.use_cases.model_predict_use_case import ModelPredictUseCase


@pytest.fixture
def mock_repository():
    repository = MagicMock()
    repository.load = AsyncMock()
    return repository


@pytest.fixture
def model_predict_use_case(mock_repository):
    return ModelPredictUseCase(model_repository=mock_repository)


@pytest.mark.asyncio
async def test_model_predict_success(model_predict_use_case, mock_repository):
    # Dados de entrada fictícios
    input_data = [[1, 2, 3], [4, 5, 6]]

    # Simulando o modelo e sua predição
    mock_model = MagicMock()
    mock_model.predict.return_value = [0, 1]  # Exemplo de predição

    # Simulando o carregamento do modelo
    mock_repository.load.return_value = mock_model  # Usando o mock do load
    await model_predict_use_case.load_model('path/to/model.pkl')

    # Chamando a predição
    predictions = await model_predict_use_case(input_data)

    # Verificando a predição
    assert predictions == [0, 1]
    mock_model.predict.assert_called_once_with(input_data)


@pytest.mark.asyncio
async def test_model_predict_no_model_loaded(model_predict_use_case):
    input_data = [[1, 2, 3]]

    # Verificando se a exceção é levantada quando o modelo não está carregado
    with pytest.raises(ValueError, match='No model is loaded'):
        await model_predict_use_case(input_data)
