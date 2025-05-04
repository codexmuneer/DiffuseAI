import os
import time
import requests
import torch
from io import BytesIO
from typing import Generator, Tuple, Optional
from PIL import Image
from diffusers import StableDiffusionPipeline

class StableDiffusionModel:
    def __init__(self, use_hf_api: bool = False):
        """
        Args:
            use_hf_api: If True, uses HuggingFace API instead of local model
        """
        self.use_hf_api = use_hf_api
        
        if self.use_hf_api:
            self.hf_client = HuggingFaceClient()
        else:
            self._init_local_model()

    def _init_local_model(self):
        """Initialize local Stable Diffusion pipeline"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if self.device == "cuda" else torch.float32
        
        self.pipe = StableDiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-2-1",
            torch_dtype=torch_dtype,
            safety_checker=None,
            requires_safety_checker=False
        ).to(self.device)
        
        if self.device == "cpu":
            self.pipe.enable_sequential_cpu_offload()
            self.pipe.enable_attention_slicing()

    def generate_stream(self, prompt: str, steps: int = 20) -> Generator[Tuple[int, Image.Image], None, None]:
        """Generate images with progress streaming"""
        if self.use_hf_api:
            yield from self._generate_via_api(prompt)
        else:
            yield from self._generate_local(prompt, steps)

    def _generate_local(self, prompt: str, steps: int) -> Generator[Tuple[int, Image.Image], None, None]:
        """Local generation with progress tracking"""
        for i in range(1, steps + 1):
            image = self.pipe(
                prompt,
                num_inference_steps=i,
                output_type="pil",
                num_images_per_prompt=1
            ).images[0]
            yield int((i / steps) * 100), image

    def _generate_via_api(self, prompt: str) -> Generator[Tuple[int, Image.Image], None, None]:
        """Hugging Face API generation with mock progress"""
        try:
            yield 25, Image.new("RGB", (512, 512), color="gray")  # Progress indicator
            image_bytes = self.hf_client.generate_image(prompt)
            image = Image.open(BytesIO(image_bytes))
            yield 100, image
        except Exception as e:
            raise Exception(f"API generation failed: {str(e)}")

class HuggingFaceClient:
    def __init__(self):
        self.api_url = os.getenv(
            "HF_API_URL", 
            "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
        )
        self.headers = {
            "Authorization": f"Bearer {os.getenv('HF_API_TOKEN')}",
            "Content-Type": "application/json"
        }
        self.timeout = 30

    def generate_image(self, prompt: str) -> bytes:
        """Send request to Hugging Face inference endpoint"""
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={"inputs": prompt},
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.content
            
            if response.status_code == 503:
                # Model loading case
                estimated_time = response.json().get("estimated_time", 30)
                print(f"Model loading, waiting {estimated_time}s...")
                time.sleep(estimated_time)
                return self.generate_image(prompt)
                
            raise Exception(f"API Error {response.status_code}: {response.text}")
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
        
