#!/bin/bash
docker pull tamvlb/api_model_serving_api:latest
docker stop api_model_serving_api || true
docker rm api_model_serving_api || true
docker run -d -p 7000:7000 --name api_model_serving_api tamvlb/api_model_serving_api:latest
