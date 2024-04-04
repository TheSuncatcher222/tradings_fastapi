FROM python:3.11-slim

LABEL description="Tradings FastAPI: backend" \
      version="0.1" \
      maintainer="https://github.com/TheSuncatcher222/"

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .
