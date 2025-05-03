import grpc
from typing import Generator
from proto_files import text2img_pb2_grpc
from proto_files import text2img_pb2


class TextToImageClient:
    def __init__(self, host: str = "server", port: int = 50051):
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = text2img_pb2_grpc.TextToImageStub(self.channel)
    
    def generate_image(self, prompt: str, style: str = "") -> Generator[text2img_pb2.GenerationResponse, None, None]:
        yield from self.stub.Generate(
            text2img_pb2.GenerationRequest(prompt=prompt, style=style)
        )
    
    def enhance_prompt(self, prompt: str, enhance: bool) -> str:
        response = self.stub.EnhancePrompt(
            text2img_pb2.PromptEnhancementRequest(prompt=prompt, use_ai_enhancement=enhance)
        )
        return response.enhanced_prompt
    
    def apply_filter(self, image_data: bytes, filter_name: str) -> bytes:
        response = self.stub.ApplyFilter(
            text2img_pb2.ImageFilterRequest(image_data=image_data, filter_name=filter_name)
        )
        return response.filtered_image
    
    def generate_caption(self, image_data: bytes) -> str:
        response = self.stub.GenerateCaption(
            text2img_pb2.CaptionGenerationRequest(image_data=image_data)
        )
        return response.caption