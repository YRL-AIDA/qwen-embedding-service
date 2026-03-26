from typing import Any, AsyncGenerator, Dict, List
from fastapi import HTTPException
from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import StreamingResponse
import torch

from src.embedding.schemas import EmbedRequest, EmbedResponse
from src.embedding.dependencies import get_model_dependency
from src.embedding.utils import preprocess_messages
from src.ml.qwen3_vl_embedding import Qwen3VLEmbedder

from src.settings import settings


embedding_router = APIRouter(
    prefix=settings.EMBEDDING_PREFIX
)


async def generate_embeddings(model: Qwen3VLEmbedder, messages: List[Dict[str, str]]) -> AsyncGenerator[Any, Any]:
    """Generate and return embeddings for each message."""
    sep = ","
    for i in range(0, len(messages)):
        embedding = model.process([messages[i]])
        if i >= len(messages) - 1:
            sep = ""

        yield EmbedResponse(
            message_id=i,
            embedding=torch.squeeze(embedding).tolist()
        ).model_dump_json() + f"{sep}\n"
        

@embedding_router.post(settings.EMBED_ENDPOINT)
async def embed(request: EmbedRequest, model = Depends(get_model_dependency)) -> StreamingResponse:
    try:
        return StreamingResponse(
            generate_embeddings(model, preprocess_messages(request.messages)),
            media_type="text/plain"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
