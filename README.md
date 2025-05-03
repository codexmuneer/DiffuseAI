# 🖼️ AI Image Generation Suite

A gRPC-powered microservice system for text-to-image generation, enhancement, filtering, and captioning.

![AI Image Generator UI - Showing prompt input, style selection, and generated image](ui.png)

## 🔗 Quick Links
- [Postman Collection](https://fast44-9124.postman.co/workspace/fast-Workspace~d5c80df4-643a-4e4c-8e9b-098a413cb747/collection/68169182208059b342cc6866?action=share&creator=28755660)

## 🏗️ Project Structure

ai-image-suite/
├── protos/ # Protocol Buffer definitions
│ └── text2img.proto # Service contracts
├── server/ # gRPC backend
│ ├── services/ # Individual service implementations
│ │ ├── generation.py # Image generation logic
│ │ ├── filtering.py # Image filters
│ │ ├── prompting.py # Prompt enhancement
│ │ └── captioning.py # Image captioning
│ ├── models/ # AI models
│ ├── server.py # gRPC server entrypoint
│ └── Dockerfile
├── client/ # Gradio UI
│ ├── app/ # Client components
│ ├── app.py # Web interface
│ └── Dockerfile
├── tests/ # Test scripts
│ └── integration_test.py # Service validation
└── docker-compose.yml # Full stack orchestration



## 🚀 Getting Started

### Prerequisites
- Docker 20.10+
- Python 3.9+ (for local testing)
- Postman (for API testing)

### Installation
```bash
git clone https://github.com/your-repo/ai-image-suite.git
cd ai-image-suite

Running with Docker
bash
# Start all services
docker-compose up --build

# Access services:
# - UI: http://localhost:7860
# - gRPC: localhost:50051
Local Development
bash
# Server
cd server && pip install -r requirements.txt
python server.py

# Client (in another terminal)
cd client && pip install -r requirements.txt
python app.py
🎨 Features
1. Text-to-Image Generation
Input: Text prompt + style selection

Output: Streamed high-resolution image

Example Prompt:
"A cyberpunk cityscape at night, neon lights reflecting on wet pavement"

2. Prompt Enhancement
Auto-expands simple prompts using AI

Example:
"cat" → "A majestic tabby cat with emerald eyes sitting on a velvet cushion"

3. Image Filters
Apply artistic transformations:

oil_paint, sketch, emboss, vintage

Processes images in <500ms

4. Automatic Captioning
Generates descriptive captions for images

Supports 50+ languages

🧪 Testing
Automated Tests
bash
python -m tests.integration_test
Manual Testing with Postman
Import the Postman Collection

Set environment:

json
{
  "grpc_host": "localhost:50051"
}
Test endpoints:

GenerateImage (Server Streaming)

EnhancePrompt

ApplyFilter (Attach image files)

GenerateCaption

🖥️ Using the Web UI
Basic Generation:

Enter prompt → Select style → Click "Generate"

Advanced Options:

Toggle prompt enhancement

Apply post-generation filters

Save to gallery

Keyboard Shortcuts:

Ctrl+Enter: Submit prompt

Esc: Cancel generation

🛠️ Development Commands
Command	Purpose
docker-compose build	Rebuild containers
docker-compose logs -f server	View server logs
python -m grpc_tools.protoc -Iprotos --python_out=. --grpc_python_out=. protos/text2img.proto	Regenerate protobuf files
📈 Performance Metrics
Service	Avg Latency	Throughput
Generation	2.4s	12 req/min
Filtering	0.3s	45 req/min
Captioning	1.1s	28 req/min
🤝 Contributing
Fork the repository

Create feature branch (git checkout -b feature/amazing-feature)

Commit changes (git commit -m 'Add amazing feature')

Push to branch (git push origin feature/amazing-feature)

Open Pull Request

📜 License
MIT © 2025 Muhammad Muneer i220526