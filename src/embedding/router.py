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

import logging



logger = logging.getLogger(__name__)


embedding_router = APIRouter(
    prefix=settings.EMBEDDING_PREFIX
)


async def generate_embeddings(model: Qwen3VLEmbedder, messages: List[Dict[str, str]]) -> AsyncGenerator[Any, Any]:
    """Generate and return embeddings for each message."""
    for i in range(0, len(messages)):
        error_msg = None
        try:
            embedding = model.process([messages[i]])
            embedding_list = torch.squeeze(embedding).tolist()
        except ValueError as e:
            error_msg = f"Error generating embedding for message {i}: {e}"
            logger.exception(error_msg)
            
            embedding_list = [0.0] * settings.vl_model_output_dim
            
        response = EmbedResponse(
            message_id=i,
            embedding=embedding_list,
            error_msg=error_msg
        ).model_dump_json()
        
        sep = "," if i < len(messages) - 1 else ""
        yield f"{response}{sep}\n"
        

@embedding_router.post(settings.EMBED_ENDPOINT)
async def embed(request: EmbedRequest, model = Depends(get_model_dependency)) -> StreamingResponse:
    try:
        return StreamingResponse(
            generate_embeddings(model, preprocess_messages(request.messages)),
            media_type="text/plain"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during embedding generation: {e}")
        raise HTTPException(status_code=500, detail=str(e))
