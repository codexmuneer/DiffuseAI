import grpc
import os
from io import BytesIO
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
from proto_files.text2img_pb2 import GenerationResponse
from proto_files.text2img_pb2_grpc import TextToImageServicer
from models.stable_diffusion import StableDiffusionModel

class GenerationService(TextToImageServicer):
    def __init__(self):
        # Determine which mode to use (default to API if token exists)
        # use_hf_api = os.getenv("HF_API_TOKEN") is not None
        self.model = StableDiffusionModel(use_hf_api=True)
        
        # Warm up the model
        self._warmup_model()

    def _warmup_model(self):
        """Generate a test image to initialize the model"""
        try:
            next(self.model.generate_stream("warmup", steps=1))
        except Exception as e:
            print(f"Model warmup failed: {str(e)}")

    def Generate(self, request, context):
        if not request.prompt.strip():
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Prompt cannot be empty"
            )

        try:
            for progress, image in self.model.generate_stream(request.prompt):
                with BytesIO() as buffer:
                    image.save(buffer, format="PNG")
                    yield GenerationResponse(
                        chunk_data=buffer.getvalue(),
                        progress=progress,
                        is_final=(progress == 100)
                    )
        except Exception as e:
            context.abort(
                grpc.StatusCode.INTERNAL,
                f"Generation failed: {str(e)}"
            )



