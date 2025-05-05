FROM python:3.9-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Cache models
ENV TRANSFORMERS_CACHE=/app/models
ENV HF_HOME=/app/models

# Install Python deps
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy protobuf definitions
COPY ..


# Copy server code
COPY server/ /app/

EXPOSE 50051

CMD ["python", "server.py"]