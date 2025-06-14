FROM python:3.9-slim

# Port will be exposed, for documentation only
EXPOSE 7000

# Define working folder
WORKDIR /app

# Copy to working folder
COPY . .
ENV PYTHONPATH=/app

#RUN apt-get update
RUN pip install --upgrade pip && \
	pip install --no-cache-dir -r app/requirements.txt psycopg2-binary


CMD ["uvicorn", "api_model_serving.app.main:app", "--host", "0.0.0.0", "--port", "7000", "--reload"]
