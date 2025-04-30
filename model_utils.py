import torch
from diffusers import StableDiffusionPipeline
from io import BytesIO

def load_model():
    return StableDiffusionPipeline.from_pretrained(
        "stabilityai/stable-diffusion-2-1-base",
        torch_dtype=torch.float16
    ).to("cuda" if torch.cuda.is_available() else "cpu")

async def generate_image(pipe, prompt: str) -> bytes:
    image = pipe(prompt).images[0]
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()