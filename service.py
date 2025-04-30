import grpc
from concurrent.futures import ThreadPoolExecutor

from hf_client import HuggingFaceClient

import text2img_pb2
import text2img_pb2_grpc



class TextToImageService(text2img_pb2_grpc.TextToImageServicer):
    def __init__(self):
        self.client = HuggingFaceClient()

    def Generate(self, request, context):
        # reject empty prompts
        if not request.prompt.strip():
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Prompt cannot be empty"
            )

        try:
            # call your HF client
            image_bytes = self.client.generate_image(request.prompt)
            return text2img_pb2.GenerationResponse(image_data=image_bytes)

        except Exception as e:
            # server-side error
            context.abort(
                grpc.StatusCode.INTERNAL,
                f"Failed to generate image: {e}"
            )


def serve():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    text2img_pb2_grpc.add_TextToImageServicer_to_server(
        TextToImageService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server listening on 50051…")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
