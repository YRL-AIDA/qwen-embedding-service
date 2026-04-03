import base64
from io import BytesIO
from typing import Any, Dict, List
from PIL import Image

from src.embedding.schemas import Message


def base64_to_pil_image(base64_string: str) -> Image.Image:
    """Convert a base64-encoded image string to a PIL Image.

    Supports both raw base64 strings and data URL format (e.g. 'data:image/jpeg;base64,...').

    Args:
        base64_string: Base64-encoded image string, optionally prefixed with data URL.

    Returns:
        PIL Image object.

    Raises:
        ValueError: If the string is not a valid base64 or image data is corrupted.
        Exception: If decoding fails for any reason.
    """
    try:
        if "data:image" in base64_string and ";base64," in base64_string:
            base64_string = base64_string.split(",", 1)[1]

        img_bytes = base64.b64decode(base64_string, validate=True)
        return Image.open(BytesIO(img_bytes))
    except Exception as e:
        raise ValueError(f"Failed to decode base64 image: {e}") from e


def preprocess_messages(messages: List[Message]) -> List[Dict[str, Any]]:
    """Preprocess OpenAI-style messages into Qwen3VLEmbedder input format.

    Converts a list of Message objects into dictionaries expected by the embedder,
    handling different message types including text, image URLs, local images,
    and base64-encoded images.

    Args:
        messages: List of Message objects containing type, text, image_url, or image fields.

    Returns:
        List of dictionaries with keys like 'text', 'image', or both (for image/text).
        - 'text' messages contain {"text": "..."}
        - 'image_url' messages are treated as {"image": "http://..."}
        - 'image' messages contain file paths or PIL.Image objects if base64
        - 'image/text' messages contain both "image" and "text"

    Raises:
        ValueError: If an unsupported message type is encountered.
        ValueError: If base64 decoding fails in 'image' type messages.

    Note:
        This function ensures that base64 image strings are decoded into PIL Images,
        while preserving URLs and file paths as strings.
    """
    preprocessed_messages = []

    for message in messages:
        processed_msg = {
            "type": message.type,
        }
        if message.type == "image/text":
            if not message.image or not message.text:
                raise ValueError("image/text message must have both 'image' and 'text'")
            processed_msg["image"] = base64_to_pil_image(message.image) if "base64" in message.image else message.image
            processed_msg["text"] = message.text
        elif message.type == "text":
            if not message.text:
                raise ValueError("text message must contain non-empty 'text'")
            processed_msg["text"] = message.text
        elif message.type == "image_url":
            if not message.image_url:
                raise ValueError("image_url message must contain 'image_url'")
            processed_msg["image"] = message.image_url
        elif message.type == "image":
            if not message.image:
                raise ValueError("image message must contain 'image'")
            # Decode base64 to PIL image; keep path/URL as string
            processed_msg["image"] = base64_to_pil_image(message.image) if "base64" in message.image else message.image
        else:
            raise ValueError(f"Unsupported message type: {message.type}")

        preprocessed_messages.append(processed_msg)

    return preprocessed_messages
