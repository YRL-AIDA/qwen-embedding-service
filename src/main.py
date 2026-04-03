import os

from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.settings import Settings
from src.settings import settings
from src.ml.loader import load_text_model, load_vl_model, load_vl_reranker_model
from src.embedding.router import embedding_router
from src.upload.router import upload_router
from src.reranker.router import reranker_router


import logging



logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading applicatoin settings...")
    app.state.settings = Settings()

    logger.info("Creating directories...")
    os.makedirs(app.state.settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(app.state.settings.REQUEST_DIR, exist_ok=True)
    os.makedirs(app.state.settings.RESPONSE_DIR, exist_ok=True)

    
    if app.state.settings.USE_EMBEDDER:
        if app.state.settings.USE_VL:
            logger.info(f"Loading embedding model {app.state.settings.VL_MODEL_NAME}...")
            app.state.model = load_vl_model(app.state.settings.VL_MODEL_NAME)
        else:
            logger.info(f"Loading embedding model {app.state.settings.TEXT_ONLY_MODEL_NAME}...")
            app.state.model = load_text_model(
                app.state.settings.TEXT_ONLY_MODEL_NAME,
                app.state.settings.DEVICE
            )

    if app.state.settings.USE_RERANKER:
        logger.info(f"Loading reranker model {app.state.settings.RERANKER_MODEL_NAME}")
        app.state.reranker = load_vl_reranker_model(app.state.settings.RERANKER_MODEL_NAME)
        
    yield

    del app.state #.model


app = FastAPI(
    title=f"Qwen3 Text Embeddings Service", 
    version="1.0",
    lifespan=lifespan
)

# Routers 
if settings.USE_EMBEDDER:
    app.include_router(embedding_router)
if settings.USE_RERANKER:
    app.include_router(reranker_router)
app.include_router(upload_router)
