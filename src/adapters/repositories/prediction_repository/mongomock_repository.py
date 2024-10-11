from typing import Dict, List

from mongomock.mongo_client import MongoClient

from src.ports.repositories.prediction_repository import PredictionRepository


class InMemoryDatabase:
    _instance = None

    def __new__(cls) -> MongoClient:
        if cls._instance is None:
            client = MongoClient()
            cls._instance = client.get_database('memory_db')
        return cls._instance


class InMemoryPredictionRepository(PredictionRepository):
    def __init__(self):
        self._db = InMemoryDatabase()
        self._collection = self._db.get_collection('predictions')

    async def add_prediction(self, prediction: Dict) -> None:
        """Adiciona uma predição ao banco de dados"""
        self._collection.insert_one(prediction)

    async def get_all_predictions(self) -> List[Dict]:
        """Recupera todas as predições do banco de dados"""
        return list(self._collection.find({}, {'_id': 0}))

    async def clear(self):
        """Remove todas as predições do banco de dados"""
        self._collection.delete_many({})
