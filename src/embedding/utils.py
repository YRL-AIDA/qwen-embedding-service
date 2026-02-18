import base64
from io import BytesIO
from typing import Dict, List
from PIL import Image

from src.embedding.schemas import Message


def base64_to_pil_image(base64_string: str) -> Image:
    """Convert base64 string to PIL image."""
    if "data:image" in base64_string and ";base64," in base64_string:
        base64_string = base64_string.split(",")[1]
    img_bytes = base64.b64decode(base64_string)
    return Image.open(BytesIO(img_bytes))


def preprocess_messages(messages: List[Message]) -> List[Dict[str, str]]:
    """Preprocess openai message style to Qwen3VLEmbedder format."""
    preprocessed_messages = []
    for message in messages:
        type = message.type
        content = None

        if message.type == "text":
            content = message.text
        elif message.type == "image_url":
            type = "image"
            content = message.image_url
        elif message.type == "image":
            content = message.image
            if "base64" in message.image:
                content = base64_to_pil_image(message.image)
        else:
            raise Exception(f"unsupported message type: {message.type}")
        
        preprocessed_messages.append({type: content})
    return preprocessed_messages
