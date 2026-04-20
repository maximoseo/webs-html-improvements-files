FROM python:3.11-alpine
WORKDIR /app
RUN pip install --no-cache-dir openpyxl gspread google-auth
COPY index.html /app/index.html
COPY data.json /app/data.json
COPY server.py /app/server.py
COPY kwr_backend.py /app/kwr_backend.py
COPY n8n-workflow-map.json /app/n8n-workflow-map.json
EXPOSE 8000
CMD ["python", "/app/server.py"]
