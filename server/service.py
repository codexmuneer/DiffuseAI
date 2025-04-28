import asyncio
from concurrent import futures
import grpc
from proto.text2img_pb2_grpc import TextToImageServicer, add_TextToImageServicer_to_server
from proto.text2img_pb2 import GenerationRequest, GenerationResponse, Error
from model_utils import load_model, generate_image

class TextToImageService(TextToImageServicer):
    def __init__(self):
        self.pipe = load_model()
        
    async def Generate(self, request: GenerationRequest, context):
        try:
            if not request.prompt:
                raise ValueError("Empty prompt")
                
            image = await generate_image(self.pipe, request.prompt)
            return GenerationResponse(image_data=image)
            
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            return GenerationResponse(
                error=Error(message=str(e), code=grpc.StatusCode.INTERNAL.value[0])
            )

async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    add_TextToImageServicer_to_server(TextToImageService(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())