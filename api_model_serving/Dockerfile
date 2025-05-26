FROM python:3.9-slim

# Port will be exposed, for documentation only
EXPOSE 7000

# Copy to working folder
COPY app/ ./app

#RUN apt-get update
RUN pip install --upgrade pip && \
	pip install --no-cache-dir -r app/requirements.txt psycopg2-binary

# Define working folder
WORKDIR /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7000", "--reload"]
