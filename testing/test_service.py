import grpc
import unittest
from proto_files import text2img_pb2
from proto_files import text2img_pb2_grpc

class TestTextToImageAPI(unittest.TestCase):
    def setUp(self):
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = text2img_pb2_grpc.TextToImageStub(self.channel)
    
    def test_generate_image(self):
        """Test streaming image generation"""
        responses = self.stub.Generate(
            text2img_pb2.GenerationRequest(
                prompt="A cat in space",
                style="fantasy"
            )
        )
        for response in responses:
            self.assertTrue(response.progress >= 0)
            if response.is_final:
                self.assertGreater(len(response.chunk_data), 0)

    def test_enhance_prompt(self):
        response = self.stub.EnhancePrompt(
            text2img_pb2.PromptEnhancementRequest(
                prompt="a dog",
                use_ai_enhancement=True
            )
        )
        self.assertNotEqual(response.enhanced_prompt, "")

    def test_apply_filter(self):
        # Test with a small black image (1x1 pixel)
        test_image = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDAT\x08\xd7c\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xa7\x81\xe1\x00\x00\x00\x00IEND\xaeB`\x82'
        
        response = self.stub.ApplyFilter(
            text2img_pb2.ImageFilterRequest(
                image_data=test_image,
                filter_name="emboss"
            )
        )
        self.assertGreater(len(response.filtered_image), 0)

    def test_generate_caption(self):
        # Test with the same small image
        test_image = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDAT\x08\xd7c\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xa7\x81\xe1\x00\x00\x00\x00IEND\xaeB`\x82'
        
        response = self.stub.GenerateCaption(
            text2img_pb2.CaptionGenerationRequest(
                image_data=test_image
            )
        )
        self.assertNotEqual(response.caption, "")

if __name__ == "__main__":
    unittest.main()