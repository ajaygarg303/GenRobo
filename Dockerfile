ARG NODE_BASE_IMAGE=public.ecr.aws/docker/library/node:20-alpine
ARG PYTHON_BASE_IMAGE=public.ecr.aws/docker/library/python:3.12-slim

FROM ${NODE_BASE_IMAGE} AS web
WORKDIR /web
COPY frontend/package.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

FROM ${PYTHON_BASE_IMAGE}
WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
COPY --from=web /web/dist ./app/static

ENV PYTHONUNBUFFERED=1
ENV ENABLE_DOCS=false

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
