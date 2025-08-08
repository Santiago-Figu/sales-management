FROM python:3.11-slim-bookworm


EXPOSE 8010

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=/app \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev libpq-dev && \
    apt-get install -y wkhtmltopdf && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir
COPY . .

# Instalar alembic como parte de las dependencias
RUN pip install alembic

# Usuario no root
RUN adduser -u 5678 --disabled-password --gecos "" appuser && \
    chown -R appuser $APP_HOME
USER appuser