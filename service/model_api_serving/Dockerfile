FROM python:3.9-slim

# Port will be exposed, for documentation only
EXPOSE 7000

# Define working folder
WORKDIR /api_source

# Copy to working folder
COPY . .

RUN pip install --upgrade pip && \
	pip install --no-cache-dir -r api_source/requirements.txt psycopg2-binary

CMD ["uvicorn", "api_source.instrument:app", "--host", "0.0.0.0", "--port", "7000", "--reload"]
