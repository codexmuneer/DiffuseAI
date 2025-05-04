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