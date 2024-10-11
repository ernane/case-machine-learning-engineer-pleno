from abc import ABC, abstractmethod
from typing import Dict, List


class PredictionRepository(ABC):
    @abstractmethod
    async def add_prediction(self, prediction: Dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get_all_predictions(self) -> List[Dict]:
        raise NotImplementedError
