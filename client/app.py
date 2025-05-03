# import gradio as gr
# from io import BytesIO
# from PIL import Image
# from grpc_client import TextToImageClient
# # from gallery_manager import GalleryManager

# client = TextToImageClient(host="localhost", port=50051)
# # gallery = GalleryManager()

# def process_generation(prompt, style, enhance):
#     try:
#         # Step 1: Enhance prompt
#         enhanced = client.enhance_prompt(prompt, enhance)
        
#         # Step 2: Generate image with progress
#         for response in client.generate_image(enhanced, style):
#             if response.progress < 100:
#                 yield f"Generating... {response.progress}%", None, None
            
#             if response.chunk_data:
#                 img = Image.open(BytesIO(response.chunk_data))
                
#                 # Step 3: Generate caption
#                 caption = client.generate_caption(response.chunk_data)
                
#                 # # Save to gallery
#                 # gallery.save(img, caption)
                
#                 yield "Complete", img, caption
                
#     except Exception as e:
#         yield f"Error: {str(e)}", None, None

# # Gradio interface
# with gr.Blocks() as demo:
#     with gr.Row():
#         prompt = gr.Textbox(label="Prompt")
#         style = gr.Dropdown(["realistic", "fantasy", "anime"], label="Style")
#     enhance = gr.Checkbox(label="Enhance Prompt")
#     generate_btn = gr.Button("Generate")
    
#     status = gr.Textbox(label="Status")
#     image_output = gr.Image(label="Generated Image")
#     caption_output = gr.Textbox(label="Caption")

#     generate_btn.click(
#         process_generation,
#         inputs=[prompt, style, enhance],
#         outputs=[status, image_output, caption_output]
#     )

# demo.launch(server_name="0.0.0.0", server_port=7860)


import gradio as gr
from io import BytesIO
from PIL import Image
from grpc_client import TextToImageClient

client = TextToImageClient(host="localhost", port=50051)

def process_generation(prompt, style, enhance):
    try:
        enhanced_prompt = ""
        # Step 1: Enhance prompt if requested
        if enhance:
            enhanced_prompt = client.enhance_prompt(prompt, True)
            yield f"Enhanced prompt: {enhanced_prompt}", None, enhanced_prompt, None
        
        # Use enhanced prompt if available, otherwise original
        final_prompt = enhanced_prompt if enhance and enhanced_prompt else prompt
        
        # Step 2: Generate image with progress
        for response in client.generate_image(final_prompt, style):
            if response.progress < 100:
                yield f"Generating... {response.progress}%", None, enhanced_prompt if enhance else "", None
            
            if response.chunk_data and response.is_final:
                img = Image.open(BytesIO(response.chunk_data))
                caption = client.generate_caption(response.chunk_data)
                yield "Generation Complete!", img, enhanced_prompt if enhance else "", caption
                
    except Exception as e:
        yield f"Error: {str(e)}", None, "", None

# Custom CSS for dark theme
custom_css = """
:root {
    --background-fill: #000000 !important;  /* Pure black background */
    --block-background-fill: #1e1e1e;
    --block-label-background: #2a2a2a;
    --block-border-color: #444;
    --input-background: #333;
    --text-color: #ffffff;
    -text-primary: #ffffff;  /* White primary text */

}

body, .gradio-container {
    background: var(--background-fill) !important;
    color: var(--text-color) !important;
}

.gr-block {
    background: var(--block-background-fill) !important;
    border-color: var(--block-border-color) !important;
    color: var(--text-color) !important;
}

.gr-box {
    background: var(--block-background-fill) !important;
}

.gr-input, .gr-textbox, .gr-dropdown, .gr-checkbox {
    background: var(--input-background) !important;
    color: var(--text-color) !important;
    border-color: var(--block-border-color) !important;
}

.gr-button {
    background: #4CAF50 !important;
    color: white !important;
    border-radius: 4px !important;
}

h1 {
    color: #4CAF50 !important;
    text-align: center !important;
}

footer {
    visibility: hidden;
}
"""




with gr.Blocks(css=custom_css, title="AI Image Generator") as demo:
    # Project header
    gr.Markdown("""# 🎨 Text-to-Image Generator v1.1
    Create stunning AI-generated images from text prompts
    """)
    
    with gr.Row():
        with gr.Column(scale=3):
            prompt = gr.Textbox(label="Your Prompt", placeholder="Describe the image you want to generate...")
            with gr.Row():
                style = gr.Dropdown(["realistic", "fantasy", "anime"], label="Style", value="realistic")
                enhance = gr.Checkbox(label="Enhance Prompt", value=False)
            generate_btn = gr.Button("Generate Image", variant="primary")
            
        with gr.Column(scale=2):
            status = gr.Textbox(label="Status", interactive=False)
            enhanced_prompt = gr.Textbox(label="Enhanced Prompt", visible=False, interactive=False)
    
    with gr.Row():
        image_output = gr.Image(label="Generated Image", height=512)
        with gr.Column():
            caption_output = gr.Textbox(label="Image Caption", interactive=False)
    
    # Show/hide enhanced prompt based on checkbox
    enhance.change(
        fn=lambda x: gr.Textbox(visible=x),
        inputs=enhance,
        outputs=enhanced_prompt
    )
    
    generate_btn.click(
        process_generation,
        inputs=[prompt, style, enhance],
        outputs=[status, image_output, enhanced_prompt, caption_output]
    )

demo.launch(server_name="0.0.0.0", server_port=7860)