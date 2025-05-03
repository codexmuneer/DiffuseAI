from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from proto_files.text2img_pb2_grpc import TextToImageServicer
from proto_files.text2img_pb2 import PromptEnhancementResponse
from grpc import ServicerContext
import grpc


class PromptingService(TextToImageServicer):
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
        self.model = AutoModelForCausalLM.from_pretrained("distilgpt2")
        self.enhancer = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer
        )

    def EnhancePrompt(self, request, context: ServicerContext):
        if not request.prompt.strip():
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Prompt cannot be empty")
        
        try:
            if request.use_ai_enhancement:
                enhanced = self.enhancer(
                    request.prompt,
                    max_length=60,
                    num_return_sequences=1,
                    truncation=True
                )[0]['generated_text']
            else:
                enhanced = request.prompt
                
            return PromptEnhancementResponse(enhanced_prompt=enhanced)
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, f"Prompt enhancement failed: {str(e)}")