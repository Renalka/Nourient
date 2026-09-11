# Cloud Run deployment image. The public listener is Nginx; the existing FastAPI
# services remain private processes on localhost inside this one container.
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    ENVIRONMENT=production \
    HF_HOME=/opt/models \
    SENTENCE_TRANSFORMERS_HOME=/opt/models \
    PORT=8080

RUN apt-get update \
    && apt-get install -y --no-install-recommends bash curl gettext-base nginx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /tmp/requirements.txt

COPY backend /app
COPY deploy/nginx.conf.template /etc/nginx/templates/nourient.conf.template
COPY deploy/entrypoint.sh /usr/local/bin/nourient-entrypoint

# The enhanced ingredient and claims features need this embedding model. Baking
# it into the image prevents a cold-start download from Hugging Face.
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')" \
    && chmod +x /usr/local/bin/nourient-entrypoint \
    && rm -f /etc/nginx/sites-enabled/default

EXPOSE 8080

CMD ["/usr/local/bin/nourient-entrypoint"]
