import torch

from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    # Service
    SERVICE_ADDRESS: str = "0.0.0.0"
    SERVICE_PORT: int = 10115

    USE_EMBEDDER: bool = 0
    USE_RERANKER: bool = 1

    # ML
    ## EMBEDDING
    TEXT_ONLY_MODEL_NAME: str = "Qwen/Qwen3-Embedding-0.6B"
    USE_VL: bool = True
    VL_MODEL_NAME: str = "Qwen/Qwen3-VL-Embedding-2B"
    
    # TODO retrieve from model config
    VL_MODEL_OUTPUT_DIM: int = 2048
    MAX_SEQ_LENGTH: int = 8192
    DEVICE: str = "cuda" if torch.cuda.is_available() else "cpu"

    #Reranker
    RERANKER_MODEL_NAME: str = "Qwen/Qwen3-VL-Reranker-2B"

    # Routes
    EMBEDDING_PREFIX: str = "/embedding"
    EMBED_ENDPOINT: str = "/embed"
    EMBED_URL: str = f"http://{SERVICE_ADDRESS}:{SERVICE_PORT}{EMBEDDING_PREFIX}{EMBED_ENDPOINT}"

    UPLOAD_PREFIX: str = "/upload"
    UPLOAD_ENDPOINT: str = "/upload-image"
    UPLOAD_URL: str = f"http://{SERVICE_ADDRESS}:{SERVICE_PORT}{UPLOAD_PREFIX}{UPLOAD_ENDPOINT}"

    RERANKER_PREFIX: str = "/reranker"
    RERANK_ENDPOINT: str = "/rerank"
    RERANK_URL: str = f"http://{SERVICE_ADDRESS}:{SERVICE_PORT}{RERANKER_PREFIX}{RERANK_ENDPOINT}"

    # Files
    UPLOAD_DIR: str ="uploads/"
    REQUEST_DIR: str="requests/"
    RESPONSE_DIR: str ="responses/"

    # JSON
    encoding: str = "utf-8"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )



settings = Settings()
