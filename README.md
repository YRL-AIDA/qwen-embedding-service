# Qwen3 Embedding Service
A lightweight, embedding microservice powered by Alibaba's Qwen3-Embedding models.

## Quick start
### 1. Setup docker container
```bash
# build image
docker build --pull -t qwen3-emb-service .

# run service (cpu)
docker run -p $HOST_PORT:$CONTAINER_PORT -e HF_TOKEN="$HF_TOKEN" qwen3-emb-service

# run service (gpu) (requires NVIDIA container toolkit: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
docker run --gpus 1 -p $HOST_PORT:$CONTAINER_PORT -e HF_TOKEN="$HF_TOKEN" qwen3-emb-service
```

### 2. Test API
Option #1:
```bash
curl -X POST http://0.0.0.0:{$HOST_PORT}/embedding/embed \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"type": "text", "text": "What is RAG?"}]}'
```

Option #2:
```bash
uv run evaluate.py
```

You'll get a JSON response `/responses/response.json` with L2-normalized embeddings.


## API reference
- **input**: list of strings (or dict)
- **output**: list of L2-normalized embeddings
- **model**: Qwen3-Embedding-`X`B / Qwen3-VL-Embedding-`X`B


`POST /embeddings/embed`:
```json
{
  "messages": [
    {"type": "text", "text": "Text document #1"},
    {"type": "image_url", "image_url": "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg"},
    {"type": "image", "image": "uploads/demo.jpeg"}
  ]
}
```

## Image format
1. Images can be passed as URL. For example: https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg
2. Upload images into `uploads` directory and pass filename. For example for image `./uploads/demo.jpg`, in JSON you should pass `uploads/demo.jpg`. 
3. Image in base64 format, for example: `data:image/jpeg;base64,\9J3fklg...`.

See `evalueate.py`.

## Embedding dimensions
Qwen3 Embedding models have user defined output size. You can change `hidden_size` in `config.json` for specific model.

For example, `Qwen/Qwen3-VL-Embedding-2B` supports user-defined output dimensions ranging from 64 to 2048.

## Switch between Text only model and VL model
To load VL model, you need to set `VL = True` in `src/core/settings.py`. Use `False` to load text only model.
