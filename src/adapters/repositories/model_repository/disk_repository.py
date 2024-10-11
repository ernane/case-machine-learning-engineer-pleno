import os
import pickle

from src.adapters.repositories.exceptions import (
    ModelLoadingError,
    ModelNotFoundError,
    ModelUnpicklingError,
)
from src.ports.repositories.model_repository import ModelRepository


class DiskModelRepository(ModelRepository):
    @staticmethod
    async def load(path: str):
        try:
            if not os.path.exists(path):
                raise ModelNotFoundError(path)

            with open(path, 'rb') as f:
                return pickle.load(f)

        except FileNotFoundError:
            raise ModelNotFoundError(path)
        except pickle.UnpicklingError as e:
            raise ModelUnpicklingError(path, e)
        except Exception as e:
            raise ModelLoadingError(path, e)

    @staticmethod
    async def save(model, path: str):
        try:
            # Salva o modelo no caminho especificado
            with open(path, 'wb') as f:
                pickle.dump(model, f)
            return True
        except Exception as e:
            raise Exception(f'An error occurred while saving the model: {e}')
