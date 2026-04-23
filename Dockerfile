FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt* ./
RUN pip install --no-cache-dir -r requirements.txt 2>/dev/null || pip install --no-cache-dir openpyxl pandas requests fpdf2 sentry-sdk
COPY . .
ENV PYTHONUNBUFFERED=1 PORT=8000 R5_DATA_DIR=/data/r5
RUN mkdir -p /data/r5
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl -fsS http://localhost:8000/health || exit 1
CMD ["python", "server.py"]
