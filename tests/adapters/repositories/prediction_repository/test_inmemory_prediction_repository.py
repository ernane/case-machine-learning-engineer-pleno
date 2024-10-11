import pytest

from src.adapters.repositories.prediction_repository.mongomock_repository import (  # noqa: E501
    InMemoryPredictionRepository,
)


@pytest.fixture
def prediction_repository():
    repository = InMemoryPredictionRepository()
    return repository


@pytest.mark.asyncio
async def test_add_prediction(prediction_repository):
    # Limpar o repositório antes do teste
    await prediction_repository.clear()

    # Dado um exemplo de entrada e predição
    prediction_entry = {
        'input': [[1, 2, 3], [4, 5, 6]],
        'predicted': [3, 3],  # Exemplo de predição
    }

    # Quando a predição é adicionada ao repositório
    await prediction_repository.add_prediction(prediction_entry)

    # Então o repositório deve conter a predição
    history = await prediction_repository.get_all_predictions()
    assert len(history) == 1
    assert history[0]['input'] == [[1, 2, 3], [4, 5, 6]]
    assert history[0]['predicted'] == [3, 3]


@pytest.mark.asyncio
async def test_get_all_predictions(prediction_repository):
    # Limpar o repositório antes do teste
    await prediction_repository.clear()

    # Dado um repositório vazio
    history = await prediction_repository.get_all_predictions()
    assert len(history) == 0

    # Quando adicionamos duas predições
    prediction_entry_1 = {'input': [[1, 2, 3]], 'predicted': [3]}
    prediction_entry_2 = {'input': [[4, 5]], 'predicted': [2]}

    await prediction_repository.add_prediction(prediction_entry_1)
    await prediction_repository.add_prediction(prediction_entry_2)

    # Então o repositório deve retornar ambas as predições
    history = await prediction_repository.get_all_predictions()
    assert len(history) == 2  # noqa: PLR2004
    assert history[0]['input'] == [[1, 2, 3]]
    assert history[0]['predicted'] == [3]
    assert history[1]['input'] == [[4, 5]]
    assert history[1]['predicted'] == [2]
