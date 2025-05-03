# import grpc
# from concurrent.futures import ThreadPoolExecutor

# from hf_client import HuggingFaceClient


# from proto_files import text2img_pb2
# from proto_files import text2img_pb2_grpc


# class TextToImageService(text2img_pb2_grpc.TextToImageServicer):
#     def __init__(self):
#         self.client = HuggingFaceClient()

#     def Generate(self, request, context):
#         # reject empty prompts
#         if not request.prompt.strip():
#             context.abort(
#                 grpc.StatusCode.INVALID_ARGUMENT,
#                 "Prompt cannot be empty"
#             )

#         try:
#             # call your HF client
#             image_bytes = self.client.generate_image(request.prompt)
#             return text2img_pb2.GenerationResponse(image_data=image_bytes)

#         except Exception as e:
#             # server-side error
#             context.abort(
#                 grpc.StatusCode.INTERNAL,
#                 f"Failed to generate image: {e}"
#             )


# def serve():
#     server = grpc.server(ThreadPoolExecutor(max_workers=10))
#     text2img_pb2_grpc.add_TextToImageServicer_to_server(
#         TextToImageService(), server
#     )
#     server.add_insecure_port("[::]:50051")
#     server.start()
#     print("gRPC server listening on 50051…")
#     server.wait_for_termination()


# if __name__ == "__main__":
#     serve()




import grpc
from concurrent import futures
from services.generation import GenerationService
from services.filtering import FilteringService
from services.prompting import PromptingService
from services.captioning import CaptioningService
from proto_files import text2img_pb2_grpc


class UnifiedTextToImageService(text2img_pb2_grpc.TextToImageServicer):
    def __init__(self):
        # Initialize all service components
        self.generation_svc = GenerationService()
        self.filtering_svc = FilteringService()
        self.prompting_svc = PromptingService()
        self.captioning_svc = CaptioningService()

    def Generate(self, request, context):
        """Handle image generation requests"""
        try:
            return self.generation_svc.Generate(request, context)
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, f"Generation failed: {str(e)}")

    def ApplyFilter(self, request, context):
        """Handle image filter requests"""
        try:
            return self.filtering_svc.ApplyFilter(request, context)
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, f"Filter application failed: {str(e)}")

    def EnhancePrompt(self, request, context):
        """Handle prompt enhancement requests"""
        try:
            return self.prompting_svc.EnhancePrompt(request, context)
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, f"Prompt enhancement failed: {str(e)}")

    def GenerateCaption(self, request, context):
        """Handle image captioning requests"""
        try:
            return self.captioning_svc.GenerateCaption(request, context)
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, f"Caption generation failed: {str(e)}")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Register the unified service only once
    text2img_pb2_grpc.add_TextToImageServicer_to_server(
        UnifiedTextToImageService(),  # Single unified service instance
        server
    )
    
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server running on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()