import pickle

import boto3
import pytest
from moto import mock_aws

from src.adapters.repositories.model_repository.s3_repository import (
    S3ModelRepository,
)


@pytest.fixture
def s3_bucket():
    with mock_aws():
        s3 = boto3.client('s3', region_name='us-east-1')
        bucket_name = 'test-bucket'
        s3.create_bucket(Bucket=bucket_name)
        yield bucket_name


@pytest.mark.asyncio
async def test_save_and_load_model(s3_bucket):
    repository = S3ModelRepository(bucket_name=s3_bucket)
    model_data = {'test': 'data'}
    model_key = 'model_path.pkl'

    await repository.save(model_data, model_key)

    s3 = boto3.client('s3', region_name='us-east-1')
    response = s3.get_object(Bucket=s3_bucket, Key=model_key)
    saved_model_data = response['Body'].read()
    assert pickle.loads(saved_model_data) == model_data

    loaded_model = await repository.load(model_key)
    assert loaded_model == model_data
