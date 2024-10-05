from abc import ABC, abstractmethod


class ModelRepository(ABC):
    @abstractmethod
    async def load(self, path: str) -> bytes | None:
        raise NotImplementedError

    @abstractmethod
    async def save(self, model: bytes, path: str) -> bool:
        raise NotImplementedError
