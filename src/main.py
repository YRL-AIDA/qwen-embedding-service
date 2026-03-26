import os

from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.settings import Settings
from src.ml.loader import load_text_model, load_vl_model
from src.embedding.router import embedding_router
from src.upload.router import upload_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading settings...")
    app.state.settings = Settings()

    print("Creating directories...")
    os.makedirs(app.state.settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(app.state.settings.REQUEST_DIR, exist_ok=True)
    os.makedirs(app.state.settings.RESPONSE_DIR, exist_ok=True)

    print(f"Loading model...")
    if app.state.settings.use_vl:
        app.state.model = load_vl_model(app.state.settings.vl_model_name)
    else:
        app.state.model = load_text_model(
            app.state.settings.text_only_model_name,
            app.state.settings.device
        )

    yield

    del app.state #.model


app = FastAPI(
    title=f"Qwen3 Text Embeddings Service", 
    version="1.0", 
    lifespan=lifespan
)

# Routers 
app.include_router(embedding_router)
app.include_router(upload_router)
