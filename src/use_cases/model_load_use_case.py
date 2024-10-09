from src.ports.repositories.model_repository import ModelRepository


class ModelLoadUseCase:
    def __init__(self, model_repository: ModelRepository):
        self._model_repository = model_repository

    async def __call__(self, model_data, model_path: str):
        """Carrega e salva o modelo utilizando o repositório injetado"""
        # Salva o modelo
        await self._model_repository.save(model_data, model_path)
        # Retorna a confirmação de sucesso
        return {
            'status': 'success',
            'message': 'Model loaded successfully',
            'path': model_path,
        }
