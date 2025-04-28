import grpc
import gradio as gr
from proto.text2img_pb2 import GenerationRequest
from proto.text2img_pb2_grpc import TextToImageStub

channel = grpc.insecure_channel("server:50051")
stub = TextToImageStub(channel)

def generate(prompt: str):
    try:
        response = stub.Generate(GenerationRequest(prompt=prompt))
        if response.HasField("error"):
            return None, f"Error {response.error.code}: {response.error.message}"
        return response.image_data, None
    except Exception as e:
        return None, str(e)

gr.Interface(
    fn=generate,
    inputs="text",
    outputs=[gr.Image(type="bytes"), gr.Textbox(label="Error")],
    title="Text-to-Image Microservice Demo"
).launch(server_name="0.0.0.0")