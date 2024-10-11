# src/adapters/repositories/exceptions.py


class ModelNotFoundError(FileNotFoundError):
    """Exceção para quando o modelo não for encontrado no caminho especificado."""

    def __init__(self, path: str):
        super().__init__(f'Model file not found at path: {path}')


class ModelUnpicklingError(ValueError):
    """Exceção para erros durante o unpickling do modelo."""

    def __init__(self, path: str, original_exception: Exception):
        super().__init__(
            f'Error unpickling the model at {path}: {original_exception}'
        )


class ModelLoadingError(Exception):
    """Exceção para erros inesperados ao carregar o modelo."""

    def __init__(self, path: str, original_exception: Exception):
        super().__init__(
            f'An unexpected error occurred while loading the model from {path}: {original_exception}'
        )
