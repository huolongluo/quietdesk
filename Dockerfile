FROM python:3.12-slim
WORKDIR /app
COPY agents/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY agents /app
ENV PYTHONPATH=/app
ENV QUIETDESK_ENGINE=fixture
ENV QUIETDESK_HOST=0.0.0.0
ENV QUIETDESK_PORT=8787
EXPOSE 8787
CMD ["python", "-m", "quietdesk.server"]
