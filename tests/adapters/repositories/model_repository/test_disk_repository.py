import os
import tempfile

import pytest

from src.adapters.repositories.model_repository.disk_repository import (
    DiskModelRepository,
)


@pytest.mark.asyncio
async def test_save_and_load_model():
    model_repository = DiskModelRepository()
    model_data = {'test': 'data'}

    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, 'model.pkl')

        await model_repository.save(model_data, file_path)

        assert os.path.exists(file_path)

        loaded_model = await model_repository.load(file_path)
        assert loaded_model == model_data
