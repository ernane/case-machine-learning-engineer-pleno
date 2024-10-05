import pickle

from src.ports.repositories.model_repository import ModelRepository


class DiskModelRepository(ModelRepository):
    @staticmethod
    async def load(path: str):
        with open(path, 'rb') as f:
            return pickle.load(f)

    @staticmethod
    async def save(model, path: str):
        with open(path, 'wb') as f:
            pickle.dump(model, f)
        return True
