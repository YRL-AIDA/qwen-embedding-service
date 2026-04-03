from src.ml.qwen3_embedding import Qwen3Embedder
from src.ml.qwen3_vl_embedding import Qwen3VLEmbedder
from src.ml.qwen3_vl_reranker import Qwen3VLReranker


def load_text_model(model_name: str, device: str) -> Qwen3Embedder:
    return Qwen3Embedder(model_name, device)


def load_vl_model(model_name: str) -> Qwen3VLEmbedder:
    return Qwen3VLEmbedder(model_name)


def load_vl_reranker_model(model_name: str) -> Qwen3VLReranker:
    return Qwen3VLReranker(model_name)
