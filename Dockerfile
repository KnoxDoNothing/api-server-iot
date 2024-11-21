FROM  python:3.11.9-alpine

COPY api_server /app/api_server/
COPY docs /app/docs/
COPY config.yaml /app/
COPY requirements.txt /app/

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt


CMD ["python3", "./api_server/run.py"]