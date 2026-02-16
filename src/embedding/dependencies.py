from fastapi import Request

from src.ml.qwen3_vl_embedding import Qwen3VLEmbedder


def get_model_dependency(request: Request) -> Qwen3VLEmbedder:
    return request.app.state.model
