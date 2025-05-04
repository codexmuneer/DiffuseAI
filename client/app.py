import gradio as gr
import os
from io import BytesIO
from PIL import Image
from grpc_client import TextToImageClient

client = TextToImageClient(host="localhost", port=50051)

def process_generation(prompt, style, enhance):
    try:
        enhanced_prompt = ""
        if enhance:
            enhanced_prompt = client.enhance_prompt(prompt, True)
            yield f"Enhanced prompt: {enhanced_prompt}", None, enhanced_prompt, None

        final_prompt = enhanced_prompt if enhance and enhanced_prompt else prompt

        for response in client.generate_image(final_prompt, style):
            if response.progress < 100:
                yield f"Generating... {response.progress}%", None, enhanced_prompt if enhance else "", None

            if response.chunk_data and response.is_final:
                img = Image.open(BytesIO(response.chunk_data))

                os.makedirs("gallery", exist_ok=True)
                img_path = f"gallery/{final_prompt[:40].replace(' ', '_')}_{response.progress}.png"
                img.save(img_path)

                caption = client.generate_caption(response.chunk_data)
                yield "Generation Complete!", img, enhanced_prompt if enhance else "", caption
    except Exception as e:
        yield f"Error: {str(e)}", None, "", None

def load_gallery_images(gallery_path="gallery", max_images=20):
    images = []
    if not os.path.exists(gallery_path):
        os.makedirs(gallery_path)
    for file_name in sorted(os.listdir(gallery_path), reverse=True):
        if file_name.lower().endswith((".png", ".jpg", ".jpeg")):
            try:
                img = Image.open(os.path.join(gallery_path, file_name))
                images.append(img)
                if len(images) >= max_images:
                    break
            except Exception:
                continue
    return images

# Light minimal CSS
custom_css = """
.gradio-container {
    font-family: 'Segoe UI', sans-serif;
    padding: 0;
}
h1, h2, h3 {
    color: #2c3e50;
}
.gr-button {
    background-color: #3498db !important;
    color: white !important;
}
"""

with gr.Blocks(css=custom_css, title="AI Image Generator") as demo:
    with gr.Row():
        with gr.Column(scale=4):  # Main area
            gr.Markdown("## 🎨 Text-to-Image Generator\nGenerate stunning images from your imagination.")

            prompt = gr.Textbox(label="Prompt", placeholder="Describe the image you want...", lines=2)
            with gr.Row():
                style = gr.Dropdown(["realistic", "fantasy", "anime"], label="Style", value="realistic")
                enhance = gr.Checkbox(label="Enhance Prompt")
            generate_btn = gr.Button("Generate Image")

            with gr.Row():
                status = gr.Textbox(label="Status", interactive=False)
                enhanced_prompt = gr.Textbox(label="Enhanced Prompt", visible=False, interactive=False)

            with gr.Row():
                image_output = gr.Image(label="Generated Image", height=400)
                caption_output = gr.Textbox(label="Image Caption", interactive=False)

        with gr.Column(scale=1, min_width=300):  # Sidebar for gallery
            gr.Markdown("### 🖼️ Gallery")
            gallery_display = gr.Gallery(columns=2, height="auto", label="Recent Images", show_label=False)
            refresh_gallery = gr.Button("🔄 Refresh")
            refresh_gallery.click(load_gallery_images, outputs=gallery_display)

    enhance.change(fn=lambda x: gr.Textbox(visible=x), inputs=enhance, outputs=enhanced_prompt)
    generate_btn.click(
        process_generation,
        inputs=[prompt, style, enhance],
        outputs=[status, image_output, enhanced_prompt, caption_output]
    )

demo.launch(server_name="0.0.0.0", server_port=7860)
