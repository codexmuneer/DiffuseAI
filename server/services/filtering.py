from io import BytesIO
from PIL import Image
import grpc
from proto_files.text2img_pb2 import ImageFilterResponse
from proto_files.text2img_pb2_grpc import TextToImageServicer
from utils.image_processing import ImageProcessor

class FilteringService(TextToImageServicer):
    def ApplyFilter(self, request, context):
        try:
            img = Image.open(BytesIO(request.image_data))
            filtered_img = ImageProcessor.apply_filter(img, request.filter_name)
            
            buffer = BytesIO()
            filtered_img.save(buffer, format="PNG")
            return ImageFilterResponse(filtered_image=buffer.getvalue())
        except Exception as e:
            context.abort(
                grpc.StatusCode.INTERNAL, 
                f"Filter application failed: {str(e)}"
            )