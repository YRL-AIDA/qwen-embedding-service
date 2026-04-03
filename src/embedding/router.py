import logging
from typing import AsyncGenerator, Dict, List, Union

import torch
from fastapi import APIRouter, Depends, HTTPException

from src.embedding.schemas import *
from src.embedding.dependencies import get_model_dependency
from src.embedding.utils import preprocess_messages

from src.ml.qwen3_vl_embedding import Qwen3VLEmbedder
from src.settings import settings


logger = logging.getLogger(__name__)

embedding_router = APIRouter(prefix=settings.EMBEDDING_PREFIX)


async def generate_embeddings(
    model: Qwen3VLEmbedder, messages: List[Dict[str, str]]
) -> AsyncGenerator[str, None]:
    """
    Асинхронно генерирует эмбеддинги по одному сообщению.
    Возвращает строки в формате JSON (с запятой между, если нужно).
    Используется для экономии памяти.
    """
    for i in range(len(messages)):
        embedding = model.process([messages[i]])
        embedding_list = torch.squeeze(embedding).tolist()

        yield MessageEmbedding(
            message_id=i,
            embedding=embedding_list
        ).model_dump()


@embedding_router.post(settings.EMBED_ENDPOINT)
async def embed(
    request: EmbedRequest,
    model: Qwen3VLEmbedder = Depends(get_model_dependency)
) -> EmbedSuccessResponse:
    """
    Принимает сообщения, генерирует эмбеддинги поочерёдно (для экономии памяти),
    собирает результаты и возвращает как:
    {
        "messages": [
            {"message_id": 0, "embedding": [...], "error_msg": null},
            ...
        ]
    }
    """
    messages = preprocess_messages(request.messages)
    results: List[MessageEmbedding] = []

    try:
        async for item in generate_embeddings(model, messages):
            results.append(item)
        return EmbedSuccessResponse(messages=results)
    except ValueError as e:
        logger.exception("Failed to parse generated embedding item")
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error during embedding generation: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
