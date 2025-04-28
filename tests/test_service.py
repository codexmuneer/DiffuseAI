import pytest
from server.service import TextToImageService
from proto.text2img_pb2 import GenerationRequest

@pytest.mark.asyncio
async def test_valid_request():
    service = TextToImageService()
    response = await service.Generate(GenerationRequest(prompt="a cat"), None)
    assert response.image_data is not None

@pytest.mark.asyncio
async def test_invalid_request():
    service = TextToImageService()
    response = await service.Generate(GenerationRequest(prompt=""), None)
    assert response.error.code == 13  # INTERNAL error code