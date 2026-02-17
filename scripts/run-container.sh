#!/bin/bash

CONTAINER_NAME="qwen3-emb-service-instance"
HOST_PORT=10014
CONTAINER_PORT=8000
IMAGE_NAME="qwen3-emb-service"

echo "Starting Docker container $CONTAINER_NAME..."

# Run the container in detached mode (-d), map ports (-p), 
# name it (--name), and remove it when stopped (--rm)
docker run --gpus all -d -p $HOST_PORT:$CONTAINER_PORT -e HF_TOKEN={YOUR_HF_TOKEN} --name $CONTAINER_NAME --rm $IMAGE_NAME

echo "Container $CONTAINER_NAME is running. Access it at http://0.0.0.0:$HOST_PORT"
