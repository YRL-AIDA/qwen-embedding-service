import base64
from pathlib import Path
from PIL import Image
from io import BytesIO

from datetime import datetime
import os
import json

from fastapi import HTTPException

import requests
import torch
import torch.nn.functional as F

from src.embedding.schemas import Message
from src.settings import settings

import logging



logger = logging.getLogger(__name__)


def upload_image(image_path: str, upload_image_url: str):
    if os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
            response = requests.post(upload_image_url, files=files)
            logger.info(f"Uploaded image: {response.json()}")
    else:
        raise HTTPException(status_code=500, detail=f"Error: {image_path} not found.")


def save_base64_image(base64_string, filename):
    im = Image.open(BytesIO(base64.b64decode(base64_string)))
    im.save(filename, 'PNG')


def encode_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        image_base64_str = base64.b64encode(image_file.read())
    return f"data:image/jpeg;base64,{image_base64_str.decode()}"


def generate_vl_request(texts: list[str], image_url: list[str], images: list[str]) -> list[dict]:
    messages = []
    for t in texts:
        messages.append(
            Message(type="text", text=t).model_dump()
        )
    
    for url in image_url:
        messages.append(
            Message(type="image_url", image_url=url).model_dump()
        )
    
    for image_str in images:
        if "base64" not in image_str:
            image_path = Path(image_str)

            if image_path.is_file():
                upload_image(image_path, settings.UPLOAD_URL)
            else:
                raise Exception("Image path {image_str} doesn't exists.")
        messages.append(
            Message(type="image", image=image_str).model_dump()
        )

    payload = {
        "messages": messages
    }

    return payload


def save_request(payload: dict, filename: str) -> str:
    os.makedirs("requests/", exist_ok=True)
    
    filepath = f"requests/{filename}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    
    print(f"Generated  '{filepath}' with {len(payload["messages"])} requests.")
    return filepath


def send_request(request_filename: str):
    with open(request_filename) as f:
        payload = json.load(f)

    response = requests.post(
        settings.EMBED_URL,
        json=payload
    )

    try:
        response_json = json.loads(
            '{"messages":[' + f"{response.text}" + "]}"
        )
    except json.JSONDecodeError as e:
        print(f"Not valid JSON: {e}")

    return response_json


def save_response(response_json, filename: str = "response"):
        # Убедимся, что директория существует
        os.makedirs("responses", exist_ok=True)

        # Генерируем имя файла с датой и временем: например, responses/response_2025-04-05_15-30-45.json
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"responses/{filename}_{timestamp}.json"

        # Сохраняем JSON
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(response_json, f, indent=2, ensure_ascii=False)

        print(f"Response saved to {filename}")


def calculate_similarity(response_json):
    # Извлекаем все эмбеддинги и message_id
    embeddings = []
    message_ids = []

    for msg in response_json["messages"]:
        emb = torch.tensor(msg["embedding"])  # [dim,]
        embeddings.append(emb)
        message_ids.append(msg["message_id"])

    # Собираем в один тензор: [N, D]
    X = torch.stack(embeddings)  # N — количество сообщений, D — размер эмбеддинга

    # Нормализуем по L2 (делаем единичной длины)
    X_normalized = F.normalize(X, p=2, dim=1)

    # Вычисляем матрицу косинусных сходств: M[i, j] = cos_sim(i, j)
    similarity_matrix = torch.mm(X_normalized, X_normalized.T)  # [N, N]

    # Округлим для красоты при выводе
    similarity_matrix = similarity_matrix.cpu().numpy()

    # Выводим с подписями
    print("Cosine Similarity Matrix:")
    print("\t" + "\t".join([str(mid) for mid in message_ids]))
    for i, mid_i in enumerate(message_ids):
        row = "\t".join([f"{similarity_matrix[i, j]:.4f}" for j in range(len(message_ids))])
        print(f"{mid_i}\t{row}")
