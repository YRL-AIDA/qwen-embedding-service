from fastapi import HTTPException
from fastapi import APIRouter
from fastapi import Depends

from src.embedding.utils import preprocess_messages

from src.reranker.dependencies import get_reranker_dependency
from src.reranker.schemas import RerankRequest, RerankResponse, ResponseMessage
from src.settings import settings

import logging



logger = logging.getLogger(__name__)


reranker_router = APIRouter(
    prefix=settings.RERANKER_PREFIX
)
        

@reranker_router.post(settings.RERANK_ENDPOINT)
async def rerank(
    request: RerankRequest,
    reranker = Depends(get_reranker_dependency)
) -> RerankResponse:
    """TODO"""
    try:
        scores = reranker.process({
            "instruction": request.instruction,
            "query": request.query,
            "documents": preprocess_messages(request.messages),
            "fps": request.fps
        })

        response_messages = []
        for i, score in enumerate(scores):
            response_messages.append(ResponseMessage(
                message_id=i,
                score=score
            ))
        return RerankResponse(messages=response_messages)
    except ValueError as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Unexpected error during embedding generation: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
