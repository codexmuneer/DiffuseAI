import grpc
from io import BytesIO
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from proto_files.text2img_pb2 import CaptionGenerationResponse
from proto_files.text2img_pb2_grpc import TextToImageServicer

class CaptioningService(TextToImageServicer):
    def __init__(self):
        # Initialize BLIP model for image captioning
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    
    def GenerateCaption(self, request, context):
        try:
            # Convert bytes to PIL Image
            image = Image.open(BytesIO(request.image_data)).convert("RGB")
            
            # Generate caption
            inputs = self.processor(image, return_tensors="pt")
            outputs = self.model.generate(**inputs, max_new_tokens=50)
            caption = self.processor.decode(outputs[0], skip_special_tokens=True)
            
            return CaptionGenerationResponse(caption=caption)
            
        except Exception as e:
            context.abort(
                grpc.StatusCode.INTERNAL,
                f"Caption generation failed: {str(e)}"
            )