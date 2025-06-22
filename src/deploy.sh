#!/bin/bash

set -e  # exit on error

echo "Pulling latest image..."
docker pull tamvlb/stroke_pred_api:latest

echo "Stopping old container if exists..."
docker stop stroke_pred_api || true

echo "Removing old container if exists..."
docker rm stroke_pred_api || true

echo "Ensuring port 7000 is free..."
# Kill any container using port 7000
existing_container=$(docker ps -q --filter "publish=7000")
if [ -n "$existing_container" ]; then
    echo "Stopping container using port 7000..."
    docker stop "$existing_container"
    docker rm "$existing_container"
fi

echo "Starting new container..."
docker run -d -p 7000:7000 --name stroke_pred_api tamvlb/stroke_pred_api:latest