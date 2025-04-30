import pytest
from unittest.mock import Mock, patch
from service import TextToImageService
from protos import text2img_pb2

@pytest.fixture
def mock_hf_client():
    with patch('server.service.HuggingFaceClient') as mock:
        yield mock

def test_valid_request(mock_hf_client):
    mock_instance = mock_hf_client.return_value
    mock_instance.generate_image.return_value = b"mock_image_data"
    
    service = TextToImageService()
    response = service.Generate(text2img_pb2.GenerationRequest(prompt="valid prompt"), None)
    
    assert response.image_data == b"mock_image_data"
    assert not response.HasField("error")

def test_empty_prompt(mock_hf_client):
    service = TextToImageService()
    response = service.Generate(text2img_pb2.GenerationRequest(prompt=""), None)
    
    assert response.error.code == 3  # INVALID_ARGUMENT
    assert "empty" in response.error.message.lower()