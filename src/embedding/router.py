from fastapi import HTTPException
import json
from fastapi import APIRouter
from fastapi import Depends

from src.embedding.schemas import EmbedRequest
from src.embedding.dependencies import get_model_dependency
from src.embedding.utils import preprocess_messages


embedding_router = APIRouter(
    prefix="/embedding"
)


@embedding_router.post("/embed")
async def embed(request: EmbedRequest, model = Depends(get_model_dependency)):
    preprocessed_messages = preprocess_messages(request.messages)
    try:
        # TODO: pydantic validate check
        # TODO: batch processing
        embeddings = model.process(preprocessed_messages)
        return json.dumps({"embeddings": embeddings.tolist()})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
