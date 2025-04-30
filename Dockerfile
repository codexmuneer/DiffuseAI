FROM python:3.10-slim

WORKDIR /app

COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY proto/ /app/proto
COPY server/ /app/server
COPY .env /app/.env

RUN python -m grpc_tools.protoc -I proto --python_out=. --grpc_python_out=. proto/text2img.proto

CMD ["python", "server/service.py"]