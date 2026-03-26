import torch

from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    # Service
    service_address: str = "0.0.0.0"
    service_port: int = 8000

    # ML
    text_only_model_name: str = "Qwen/Qwen3-Embedding-0.6B"
    vl_model_name: str = "Qwen/Qwen3-VL-Embedding-2B"
    max_seq_length: int = 8192
    use_vl: bool = True
    device: str = "cuda" if torch.cuda.is_available() else "cpu"

    # Routes
    EMBEDDING_PREFIX: str = "/embedding"
    EMBED_ENDPOINT: str = "/embed"
    EMBED_URL: str = f"http://{service_address}:{service_port}{EMBEDDING_PREFIX}{EMBED_ENDPOINT}"

    UPLOAD_PREFIX: str = "/upload"
    UPLOAD_ENDPOINT: str = "/upload-image"
    UPLOAD_URL: str = f"http://{service_address}:{service_port}{UPLOAD_PREFIX}{UPLOAD_ENDPOINT}"

    # Files
    UPLOAD_DIR: str ="uploads/"
    REQUEST_DIR: str="requests/"
    RESPONSE_DIR: str ="responses/"

    # JSON
    encoding: str = "utf-8"

    class Config:
        env_file = ".env"



settings = Settings()
