#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -euo pipefail

IMAGE_NAME="qwen3-emb-service"
TAG="0.1.0"
DOCKERFILE="Dockerfile"


# The core docker build command
docker build --pull -t "$IMAGE_NAME:$TAG" -f "$DOCKERFILE" .

# Check the exit status of the previous command
if [ $? -eq 0 ]; then
    echo "--- Successfully built Docker image: $IMAGE_NAME:$TAG ---"
else
    echo "--- Docker image build failed! ---"
    exit 1
fi
