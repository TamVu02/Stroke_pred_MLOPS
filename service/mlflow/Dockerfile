FROM python:3.9-slim

ARG MLFLOW_VERSION=2.12.1

RUN pip install --no-cache-dir mlflow==${MLFLOW_VERSION} psycopg2-binary

# Create a working directory
#RUN mkdir /mlflow
WORKDIR /mlflow/

# Expose port
EXPOSE 5000

CMD mlflow server \
    --backend-store-uri ${BACKEND_STORE_URI} \
    --serve-artifacts \
    --host 0.0.0.0 \
    --port 5000
