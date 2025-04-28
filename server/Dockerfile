FROM nvidia/cuda:12.2.0-base-ubuntu22.04

WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install --no-cache-dir -r requirements.txt

COPY proto/ /app/proto
COPY server/ /app/server

RUN python3 -m grpc_tools.protoc -I proto --python_out=. --grpc_python_out=. proto/text2img.proto

CMD ["python3", "server/service.py"]