# import grpc
# import gradio as gr
# from io import BytesIO
# from PIL import Image
# import text2img_pb2
# import text2img_pb2_grpc

# # Connect to the gRPC server
# channel = grpc.insecure_channel("localhost:50051")  # or "server:50051" in Docker
# stub = text2img_pb2_grpc.TextToImageStub(channel)

# def generate(prompt: str):
#     try:
#         response = stub.Generate(text2img_pb2.GenerationRequest(prompt=prompt))
#         if response.HasField("error"):
#             return None, f"Error {response.error.code}: {response.error.message}"
        
#         image = Image.open(BytesIO(response.image_data))
#         return image, None
#     except Exception as e:
#         return None, str(e)

# # Launch the Gradio UI
# gr.Interface(
#     fn=generate,
#     inputs="text",
#     outputs=[gr.Image(type="pil"), gr.Textbox(label="Error")],
#     title="Text-to-Image"
# ).launch(server_name="0.0.0.0")




# import os
# import sqlite3
# import grpc
# import gradio as gr
# from io import BytesIO
# from datetime import datetime
# import threading

# from PIL import Image, ImageFilter, ImageOps, ImageEnhance
# import numpy as np
# from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, BlipProcessor, BlipForConditionalGeneration

# import text2img_pb2
# import text2img_pb2_grpc

# # --- gRPC client setup ---
# channel = grpc.insecure_channel("localhost:50051")  # or "server:50051" in Docker
# stub = text2img_pb2_grpc.TextToImageStub(channel)

# # --- SQLite gallery setup ---
# DB_PATH = "gallery.db"
# IMAGE_DIR = "gallery"
# os.makedirs(IMAGE_DIR, exist_ok=True)
# # Allow SQLite connection across threads
# db_conn = sqlite3.connect(DB_PATH, check_same_thread=False)
# db_cursor = db_conn.cursor()
# # Use a lock for thread-safe DB writes
# db_lock = threading.Lock()
# # Ensure table exists
# db_cursor.execute("""
#     CREATE TABLE IF NOT EXISTS images (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         prompt TEXT,
#         full_prompt TEXT,
#         template TEXT,
#         filter TEXT,
#         timestamp TEXT,
#         filepath TEXT,
#         caption TEXT
#     )
# """)
# db_conn.commit()
# # Database migration: add full_prompt if missing
# db_columns = [row[1] for row in db_cursor.execute("PRAGMA table_info(images)")]
# if 'full_prompt' not in db_columns:
#     db_cursor.execute("ALTER TABLE images ADD COLUMN full_prompt TEXT")
#     db_conn.commit()

# # --- Initialize NLP models ---
# # Prompt enhancer: distilgpt2 for paraphrasing/expansion
# paraphrase_tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
# paraphrase_model = AutoModelForCausalLM.from_pretrained("distilgpt2")
# enhancer = pipeline("text-generation", model=paraphrase_model, tokenizer=paraphrase_tokenizer)

# # Captioner: BLIP for offline image captioning
# caption_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
# caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
# # Explicit tokenizer and processor for pipeline
# tokenizer = caption_processor.tokenizer
# image_processor = caption_processor.image_processor
# captioner = pipeline(
#     "image-to-text",
#     model=caption_model,
#     tokenizer=tokenizer,
#     image_processor=image_processor
# )

# # --- Feature definitions ---
# PROMPT_TEMPLATES = [
#     "",  # no template
#     "A fantasy landscape of [subject] in [style]",
#     "A cyberpunk scene of [subject] at night",
#     "A watercolor painting of [subject]",
# ]
# FILTERS = ["None", "Sketch", "Emboss", "Oil Paint", "Posterize", "Vintage"]

# # --- Utility functions ---
# def apply_filter(img: Image.Image, filter_name: str) -> Image.Image:
#     if filter_name == "None":
#         return img
#     if filter_name == "Sketch":
#         gray = img.convert("L")
#         inv = ImageOps.invert(gray)
#         blur = inv.filter(ImageFilter.GaussianBlur(radius=10))
#         arr_gray = np.array(gray).astype("float")
#         arr_blur = np.array(blur).astype("float")
#         dodge = np.clip(arr_gray * 255 / (255 - arr_blur + 1e-6), 0, 255).astype("uint8")
#         return Image.fromarray(dodge).convert("RGB")
#     if filter_name == "Emboss":
#         return img.filter(ImageFilter.EMBOSS)
#     if filter_name == "Oil Paint":
#         return img.filter(ImageFilter.ModeFilter(size=5))
#     if filter_name == "Posterize":
#         return ImageOps.posterize(img, bits=3)
#     if filter_name == "Vintage":
#         enhancer_c = ImageEnhance.Contrast(img)
#         img2 = enhancer_c.enhance(0.9)
#         return ImageOps.colorize(img2.convert("L"), black="#40210f", white="#f0e5d8")
#     return img

# # --- Main generation function ---
# def generate(
#     prompt: str,
#     template: str,
#     enhance_prompt: bool,
#     quick_preview: bool,
#     filter_name: str
# ):
#     # Original user prompt
#     users_prompt = prompt.strip()

#     # Build full prompt: apply template
#     full_prompt = users_prompt
#     if template and '[' in template:
#         full_prompt = template.replace('[subject]', users_prompt).replace('[style]', 'vivid')

#     # Optional paraphrase/enhance
#     if enhance_prompt and users_prompt:
#         result = enhancer(full_prompt, max_length=60, num_return_sequences=1, truncation=True)
#         full_prompt = result[0]['generated_text']
#         print("full_prompt: ", full_prompt)

#     # Make gRPC request
#     req = text2img_pb2.GenerationRequest(prompt=full_prompt)
#     resp = stub.Generate(req)
#     if resp.HasField("error"):
#         return None, "", "", f"Error {resp.error.code}: {resp.error.message}"

#     # Load image
#     img = Image.open(BytesIO(resp.image_data)).convert("RGB")

#     # Quick preview thumbnail
#     if quick_preview:
#         thumb = img.copy()
#         thumb.thumbnail((128, 128))
#         img = thumb

#     # Apply local filter
#     img = apply_filter(img, filter_name)

#     # Save locally
#     timestamp = datetime.utcnow().isoformat()
#     filename = f"img_{timestamp.replace(':','-')}.png"
#     filepath = os.path.join(IMAGE_DIR, filename)
#     img.save(filepath)

#     # Generate caption
#     caption = captioner(img, max_new_tokens=50)[0]['generated_text']

#     # Record in database
#     with db_lock:
#         db_cursor.execute(
#             "INSERT INTO images (prompt, full_prompt, template, filter, timestamp, filepath, caption) VALUES (?, ?, ?, ?, ?, ?, ?)",
#             (users_prompt, full_prompt, template, filter_name, timestamp, filepath, caption)
#         )
#         db_conn.commit()

#     # Return outputs
#     return img, full_prompt, caption, ""

# # --- Gradio UI ---
# demo = gr.Interface(
#     fn=generate,
#     inputs=[
#         gr.Textbox(lines=2, placeholder="Enter your prompt...", label="Prompt"),
#         gr.Dropdown(PROMPT_TEMPLATES, label="Prompt Template"),
#         gr.Checkbox(label="Enhance Prompt (Paraphrase/Expand)"),
#         gr.Checkbox(label="Quick Preview (Thumbnail)"),
#         gr.Dropdown(FILTERS, label="Post-Processing Filter")
#     ],
#     outputs=[
#         gr.Image(type="pil", label="Generated Image"),
#         gr.Textbox(label="Full Prompt Used"),
#         gr.Textbox(label="Caption"),
#         gr.Textbox(label="Error")
#     ],
#     title="Advanced Text-to-Image Microservice",
#     description="Includes prompt templates, local paraphrasing, quick preview, filters, gallery, and captions."
# )

# if __name__ == "__main__":
#     demo.launch(server_name="0.0.0.0", server_port=7860)


import os
import sqlite3
import grpc
import gradio as gr
from io import BytesIO
from datetime import datetime
import threading

from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import numpy as np
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, BlipProcessor, BlipForConditionalGeneration

import text2img_pb2
import text2img_pb2_grpc

# --- gRPC client setup ---
channel = grpc.insecure_channel("localhost:50051")
stub = text2img_pb2_grpc.TextToImageStub(channel)

# --- SQLite gallery setup ---
DB_PATH = "gallery.db"
IMAGE_DIR = "gallery"
os.makedirs(IMAGE_DIR, exist_ok=True)
# Allow SQLite connection across threads
db_conn = sqlite3.connect(DB_PATH, check_same_thread=False)
db_cursor = db_conn.cursor()
# Thread-safe lock for DB writes
db_lock = threading.Lock()
# Ensure table exists
db_cursor.execute("""
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prompt TEXT,
        full_prompt TEXT,
        template TEXT,
        filter TEXT,
        timestamp TEXT,
        filepath TEXT,
        caption TEXT
    )
""")
db_conn.commit()
# Migrate if needed
cols = [r[1] for r in db_cursor.execute("PRAGMA table_info(images)")]
if 'full_prompt' not in cols:
    db_cursor.execute("ALTER TABLE images ADD COLUMN full_prompt TEXT")
    db_conn.commit()

# --- Initialize models ---
# Prompt enhancer
paraphrase_tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
paraphrase_model = AutoModelForCausalLM.from_pretrained("distilgpt2")
enhancer = pipeline("text-generation", model=paraphrase_model, tokenizer=paraphrase_tokenizer)
# Captioner
caption_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
captioner = pipeline(
    "image-to-text",
    model=caption_model,
    tokenizer=caption_processor.tokenizer,
    image_processor=caption_processor.image_processor
)

# --- Features ---
PROMPT_TEMPLATES = [
    "",  # no template
    "A fantasy landscape of [subject] in [style]",
    "A cyberpunk scene of [subject] at night",
    "A watercolor painting of [subject]",
]
FILTERS = ["None", "Sketch", "Emboss", "Oil Paint", "Posterize", "Vintage"]

# --- Utilities ---
def apply_filter(img: Image.Image, name: str) -> Image.Image:
    if name == "Sketch":
        gray = img.convert("L")
        inv = ImageOps.invert(gray)
        blur = inv.filter(ImageFilter.GaussianBlur(radius=10))
        g = np.array(gray, float)
        b = np.array(blur, float)
        dodge = np.clip(g * 255 / (255 - b + 1e-6), 0, 255).astype('uint8')
        return Image.fromarray(dodge).convert("RGB")
    if name == "Emboss": return img.filter(ImageFilter.EMBOSS)
    if name == "Oil Paint": return img.filter(ImageFilter.ModeFilter(size=5))
    if name == "Posterize": return ImageOps.posterize(img, bits=3)
    if name == "Vintage":
        e = ImageEnhance.Contrast(img).enhance(0.9)
        return ImageOps.colorize(e.convert("L"), black="#40210f", white="#f0e5d8")
    return img

# Fetch gallery images
def fetch_gallery():
    db_cursor.execute("SELECT filepath FROM images ORDER BY id DESC")
    paths = [row[0] for row in db_cursor.fetchall()]
    imgs = []
    for p in paths:
        try:
            imgs.append(Image.open(p).convert("RGB"))
        except:
            continue
    return imgs

# Generate function as a streaming generator
def generate(prompt, template, enhance, quick, filt):
    user_p = prompt.strip()
    # Build full prompt
    full = user_p
    if template and '[' in template:
        full = template.replace('[subject]', user_p).replace('[style]', 'vivid')
    if enhance and user_p:
        res = enhancer(full, max_length=60, num_return_sequences=1, truncation=True)
        full = res[0]['generated_text']
    # Yield full prompt immediately
    yield None, full, '', [], ''
    # gRPC image generation
    req = text2img_pb2.GenerationRequest(prompt=full)
    res_img = stub.Generate(req)
    if res_img.HasField('error'):
        yield None, full, '', [], f"Error {res_img.error.code}: {res_img.error.message}"
        return
    img = Image.open(BytesIO(res_img.image_data)).convert("RGB")
    if quick:
        img.thumbnail((128,128))
    img = apply_filter(img, filt)
    # Yield image after generation
    yield img, full, '', [], ''
    # Caption
    cap = captioner(img, max_new_tokens=50)[0]['generated_text']
    # Save and record
    ts = datetime.utcnow().isoformat()
    fname = f"img_{ts.replace(':','-')}.png"
    path = os.path.join(IMAGE_DIR, fname)
    img.save(path)
    with db_lock:
        db_cursor.execute(
            "INSERT INTO images (prompt, full_prompt, template, filter, timestamp, filepath, caption) VALUES (?,?,?,?,?,?,?)",
            (user_p, full, template, filt, ts, path, cap)
        )
        db_conn.commit()
    # Yield caption
    yield img, full, cap, [], ''
    # Yield full gallery
    gallery = fetch_gallery()
    yield img, full, cap, gallery, ''

# --- UI with dark theme and responsive gallery ---
css = """
body {
  background-color: #121212;
  color: #e0e0e0;
}
.gradio-container {
  width: 90vw !important;
  max-width: none !important;
  margin: auto;
  padding: 20px;
}
.gradio-row {
  gap: 20px;
}
.gradio-column {
  background-color: #1e1e1e;
  border-radius: 8px;
  padding: 15px;
}
.gradio-button, .gradio-textbox, .gradio-dropdown, .gradio-checkbox {
  background-color: #2a2a2a !important;
  color: #e0e0e0 !important;
  border: 1px solid #333 !important;
}
.gradio-button {
  border-radius: 4px;
  padding: 10px 20px;
}
"""

demo = gr.Blocks(css=css)
with demo:
    with gr.Row():
        with gr.Column(scale=1):
            inp = gr.Textbox(lines=2, label="Prompt")
            tpl = gr.Dropdown(PROMPT_TEMPLATES, label="Prompt Template")
            enh = gr.Checkbox(label="Enhance Prompt")
            qv = gr.Checkbox(label="Quick Preview")
            flt = gr.Dropdown(FILTERS, label="Filter")
            btn = gr.Button("Generate")
        with gr.Column(scale=1):
            out_img = gr.Image(type="pil", label="Generated Image")
            out_full = gr.Textbox(label="Full Prompt")
            out_cap = gr.Textbox(label="Caption")
            out_err = gr.Textbox(label="Error")
        gallery = gr.Gallery(label="Gallery", columns=4)
        gallery = gr.Gallery(label="Gallery", columns=4)
    # Populate gallery on load
    demo.load(fetch_gallery, None, gallery)
    # Use queue to emit outputs incrementally as each step completes
    btn.click(
        fn=generate,
        inputs=[inp, tpl, enh, qv, flt],
        outputs=[out_img, out_full, out_cap, gallery, out_err],
        queue=True
    )

demo.launch(server_name="0.0.0.0", server_port=7860, share=False)

