FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY pyproject.toml readme.md ./
COPY src ./src

RUN pip install --upgrade pip \
    && pip install -e .

COPY . .

CMD ["politicos", "scan-sanctions"]