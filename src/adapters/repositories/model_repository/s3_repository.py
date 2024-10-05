import pickle

import boto3

from src.ports.repositories.model_repository import ModelRepository


class S3ModelRepository(ModelRepository):
    def __init__(self, bucket_name: str, region_name: str = 'us-east-1'):
        self.s3 = boto3.client('s3', region_name=region_name)
        self.bucket_name = bucket_name

    async def save(self, model, path: str):
        model_data = pickle.dumps(model)
        self.s3.put_object(Bucket=self.bucket_name, Key=path, Body=model_data)

    async def load(self, path: str):
        response = self.s3.get_object(Bucket=self.bucket_name, Key=path)
        model_data = response['Body'].read()
        return pickle.loads(model_data)
