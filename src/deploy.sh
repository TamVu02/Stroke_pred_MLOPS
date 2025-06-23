#!/bin/bash

export DOCKER_COMPOSE_DIR=./service/model_api_serving/docker-compose.yaml

set -e  # exit on error

echo "Stopping old container if exists..."
docker stop stroke_pred_api || true

echo "Removing old container if exists..."
docker rm stroke_pred_api || true

echo "Remove old images"
docker image rm tamvlb/stroke_pred_api:latest

echo "Pulling latest image..."
docker pull tamvlb/stroke_pred_api:latest

echo "Ensuring port 7000 is free..."
# Kill any container using port 7000
existing_container=$(docker ps -q --filter "publish=7000")
if [ -n "$existing_container" ]; then
    echo "Stopping container using port 7000..."
    docker stop "$existing_container"
    docker rm "$existing_container"
fi

echo "Starting new container..."
echo $DOCKER_COMPOSE_DIR
set -x
docker-compose -f ${DOCKER_COMPOSE_DIR} up -d