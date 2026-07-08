FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Patch the base image and create an unprivileged user to run the app.
RUN apt-get update && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/* && \
    python -m pip install --upgrade pip setuptools wheel && \
    groupadd -r appgroup && \
    useradd -r -g appgroup appuser

# Install dependencies first so this layer is cached between code changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chown -R appuser:appgroup /app

USER appuser

# Probe /health with Python's stdlib (curl is not included in slim images).
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
