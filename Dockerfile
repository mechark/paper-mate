FROM python:3.10-slim

WORKDIR /app

RUN pip install uv

COPY requirements.txt .
RUN uv pip install --system --cache-dir /root/.cache/uv --index-strategy unsafe-best-match -r requirements.txt

COPY src ./src
