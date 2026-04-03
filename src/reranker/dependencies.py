from fastapi import Request

from src.ml.qwen3_vl_reranker import Qwen3VLReranker


def get_reranker_dependency(request: Request) -> Qwen3VLReranker:
    return request.app.state.reranker
