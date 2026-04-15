FROM python:3.11-alpine
WORKDIR /app
COPY index.html /app/index.html
COPY data.json /app/data.json
COPY server.py /app/server.py
COPY n8n-workflow-map.json /app/n8n-workflow-map.json
EXPOSE 8000
CMD ["python", "/app/server.py"]
