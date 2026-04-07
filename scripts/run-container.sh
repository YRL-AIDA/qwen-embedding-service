#!/bin/bash

# Load environment variables from .env file if it exists
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | awk '/=/ {print $1}')
fi

CONTAINER_NAME="qwen3-emb-service-instance"
SERVICE_PORT=${SERVICE_PORT:-10115}
CONTAINER_PORT=${CONTAINER_PORT:-8000}
# TODO: change to image name
IMAGE_NAME=${IMAGE_NAME:-qwen3-embedding-service} 
TAG=${TAG:-0.2.1}

echo "Starting Docker container $CONTAINER_NAME..."

# Run the container in detached mode (-d), map ports (-p), 
# name it (--name), and remove it when stopped (--rm)
docker run --gpus 1 -d -p $SERVICE_PORT:$CONTAINER_PORT -e HF_TOKEN="$HF_TOKEN" --name $CONTAINER_NAME --rm "$IMAGE_NAME:$TAG"

echo "Container $CONTAINER_NAME is running. Access it at http://0.0.0.0:$SERVICE_PORT"
