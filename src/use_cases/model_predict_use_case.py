from src.ports.repositories.model_repository import ModelRepository


class ModelPredictUseCase:
    def __init__(self, model_repository: ModelRepository):
        self._model_repository = model_repository
        self._model = None

    async def load_model(self, model_path: str):
        """Carrega o modelo para fazer as predições."""
        self._model = await self._model_repository.load(model_path)

    async def __call__(self, input_data):
        """Faz a predição utilizando o modelo carregado."""
        if self._model is None:
            raise ValueError('No model is loaded.')

        predictions = self._model.predict(input_data)
        return predictions
