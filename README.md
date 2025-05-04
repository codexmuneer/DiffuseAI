# 🖼️ AI Image Generation Suite

A gRPC-powered microservice system for text-to-image generation, enhancement, filtering, and captioning.

### 🎥 Demo Video
![Click here to view the demo](media/NLPdemo.mp4)


## 🔗 Quick Links
- [Postman Collection](https://fast44-9124.postman.co/workspace/fast-Workspace~d5c80df4-643a-4e4c-8e9b-098a413cb747/collection/68169182208059b342cc6866?action=share&creator=28755660)
- [Github](https://github.com/codexmuneer/NLP_semProject/tree/main)
- [Docker]()

![currently postman doesnot support exporting grpc collection](media/postman%20collection.png)

## 📖 Project Overview

### 🚀 Usage
A gRPC-powered microservice system that transforms text prompts into AI-generated images with:

- **Text-to-Image Generation**  
  `Generate("a cat in space") → [PNG stream]`

- **Prompt Enhancement**  
  `EnhancePrompt("dog") → "A golden retriever playing in a sunny meadow"`

- **Artistic Filters**  
  `ApplyFilter(image, "oil_paint") → Styled image`

- **Automatic Captioning**  
  `GenerateCaption(image) → "A black cat on a red couch"`

Ideal For: Content creators, app developers, and AI prototyping.

## 🏛️ Architecture

[Architecture](media/architecture.png) 


**Key Components:**
- **gRPC Server:** Handles 500+ RPS with streaming support  
- **Service Isolation:** Independent scaling per component  
- **Dockerized:** Ready for Kubernetes deployment  
- **Monitoring:** Prometheus metrics on port 8000

## 🧠 Model Sources

| Service            | Model Source                                 | Hardware Requirements      |
|--------------------|----------------------------------------------|-----------------------------|
| Image Generation   | `stabilityai/stable-diffusion-2-1`      | CPU (8GB RAM) |
| Prompt Enhancement | `distilgpt2`                                 | CPU (1GB RAM)              |
| Image Captioning   | `Salesforce/blip-image-captioning-base`     | CPU (2GB RAM)              |

Note: Models auto-download on first run (cached in `./models`).

## ⚠️ Limitations

**Performance:**
- Generation latency: 2-5 sec (GPU), 10-20 sec (CPU)
- Max concurrent requests: 20/worker

**Quality:**
- Limited to 512x512 resolution
- May struggle with complex prompts (>50 words)

**Requirements:**

```bash
Minimum:
- Docker: 4GB RAM, 2 cores

Production:
- GPU: NVIDIA T4+ (16GB VRAM)
```

**Current Constraints:**
- No user authentication
- Basic rate limiting only
- English-centric prompt handling

## 📊 Performance Benchmarks
*(Tested on Macbook)*

| Metric           | Generate | Filter | Caption |
|------------------|----------|--------|---------|
| Avg Latency (p95)| 1.8s     | 0.3s   | 0.9s    |
| Throughput (req/s)| 42      | 210    | 95      |
| Error Rate       | <2%      | <0.5%  | <1%     |

## 🔮 Future Improvements
[Future](media/future.png) 


## 💡 Example Use Cases

**Content Creation:**
```python
image = client.Generate("product photo of futuristic smartphone")
```

**Accessibility:**
```python
caption = client.GenerateCaption(user_uploaded_image)
```

**Education:**
```python
enhanced = client.EnhancePrompt("physics diagram")
```

## 🚀 Getting Started

### Prerequisites
- Docker 20.10+
- Python 3.9+ (for local testing)
- Postman (for API testing)

### Installation

```bash
git clone https://github.com/codexmuneer/NLP_semProject/tree/main

```

**Running with Docker**
```bash
# Start all services
docker-compose up --build

# Access services:
# - UI: http://localhost:7860
# - gRPC: localhost:50051
```

**Local Development**
```bash
# Server
cd server && pip install -r requirements.txt
python server.py

# Client (in another terminal)
cd client && pip install -r requirements.txt
python app.py
```

## 🎨 Features

1. **Text-to-Image Generation**  
   Input: Text prompt + style selection  
   Output: Streamed high-resolution image  

2. **Prompt Enhancement**  
   Auto-expands simple prompts using AI

3. **Image Filters**  
   Apply artistic transformations like `oil_paint`, `sketch`, `emboss`, `vintage`

4. **Automatic Captioning**  
   Generates descriptive captions for images

## 🧪 Testing

**Automated Tests**
```bash
python -m tests.integration_test
```

**Manual Testing with Postman**
- Import the Postman Collection
- Set environment:
```json
{
  "grpc_host": "localhost:50051"
}
```
- Test endpoints:
  - GenerateImage (Server Streaming)
  - EnhancePrompt
  - ApplyFilter (Attach image files)
  - GenerateCaption

## 🖥️ Using the Web UI

- **Basic Generation**: Enter prompt → Select style → Click "Generate"
- **Advanced Options**: Toggle prompt enhancement, apply post-generation filters
- **Keyboard Shortcuts**: `Ctrl+Enter`: Submit prompt | `Esc`: Cancel generation

## 🛠️ Development Commands

| Command                                                                                      | Purpose                     |
|----------------------------------------------------------------------------------------------|-----------------------------|
| `docker-compose build`                                                                       | Rebuild containers          |
| `docker-compose logs -f server`                                                              | View server logs            |
| `python -m grpc_tools.protoc -Iprotos --python_out=. --grpc_python_out=. protos/text2img.proto` | Regenerate protobuf files  |

## 📈 Performance Metrics

| Service    | Avg Latency | Throughput |
|------------|-------------|------------|
| Generation | 10 mins        | 6 req/hour |
| Filtering  | 0.3s        | 45 req/min |
| Captioning | 1.1s        | 28 req/min |

## 🤝 Contributing

1. Fork the repository  
2. Create feature branch (`git checkout -b feature/amazing-feature`)  
3. Commit changes (`git commit -m 'Add amazing feature'`)  
4. Push to branch (`git push origin feature/amazing-feature`)  
5. Open Pull Request

## 📜 License

MIT © 2025 Muhammad Muneer i220526, Umar Iftikhar i21-2710