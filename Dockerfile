FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim

COPY . /app

WORKDIR /app

RUN uv venv
RUN uv pip install .

# set HF_HOME to cache models in container (or mount volume)
ENV HF_HOME=/app/.cache/huggingface

EXPOSE 8000

CMD ["uv", "run", "python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
