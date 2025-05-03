# import os
# import requests
# from io import BytesIO
# from PIL import Image

# class HuggingFaceClient:
#     def __init__(self):
#         self.api_url = os.getenv("HF_API_URL", "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0")
#         self.headers = {
#             "Authorization": f"Bearer {os.getenv('HF_API_TOKEN')}"
#         }

#     def generate_image(self, prompt: str) -> bytes:
#         """Send request to Hugging Face inference endpoint"""
#         try:
#             response = requests.post(
#                 self.api_url,
#                 headers=self.headers,
#                 json={"inputs": prompt},
#                 timeout=30
#             )
            
#             if response.status_code == 200:
#                 return response.content
            
#             raise Exception(f"API Error {response.status_code}: {response.text}")
            
#         except requests.exceptions.RequestException as e:
#             raise Exception(f"Request failed: {str(e)}")