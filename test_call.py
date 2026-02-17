import requests
import json
from src.settings import settings


import json
import requests
import os

from src.settings import settings


UPLOAD_IMAGES_URL = f"http://{settings.service_address}:{settings.service_port}/{settings.upload_url}"

texts = [
        "A woman playing with her dog on a beach at sunset.",
        "What is the capital of France?",
        "Explain quantum computing in simple terms.",
        "How does photosynthesis work?",
        "What are the symptoms of the common cold?",
        "Describe the plot of 'Pride and Prejudice'.",
        "What is the Pythagorean theorem?",
        "How to bake chocolate chip cookies?",
        "What causes climate change?",
        "Who was Leonardo da Vinci?",
        "Explain the theory of relativity.",
        "What is machine learning?",
        "How do vaccines work?",
        "What is the largest planet in our solar system?",
        "Describe the water cycle.",
        "What is blockchain technology?",
        "How to tie a tie?",
        "What are the benefits of regular exercise?",
        "Explain the greenhouse effect.",
        "Who wrote 'Romeo and Juliet'?",
        "What is the speed of light?",
        "How does a car engine work?",
        "What is the Fibonacci sequence?",
        "Describe the process of mitosis.",
        "What are renewable energy sources?",
        "How to write a cover letter?",
        "What is the periodic table?",
        "Explain Newton's laws of motion.",
        "What is the human genome project?",
        "How do airplanes fly?",
        "What is artificial intelligence?",
        "Describe the French Revolution.",
        "What are the stages of sleep?",
        "How to grow tomatoes at home?",
        "What is the Big Bang theory?",
        "Explain the concept of supply and demand.",
        "What is the tallest mountain in the world?",
        "How does the internet work?",
        "What are the main types of clouds?",
        "Describe the circulatory system.",
        "What is cryptocurrency?",
        "How to meditate for beginners?",
        "What is the difference between weather and climate?",
        "Explain the process of digestion.",
        "What are the seven wonders of the ancient world?",
        "How to change a flat tire?",
        "What is the function of DNA?",
        "Describe the life cycle of a butterfly.",
        "What is the Richter scale?",
        "How do solar panels work?",
        "What is the meaning of life?"
    ]

images = [
    "/home/kirilltobola/Downloads/demo.jpeg",
    "/home/kirilltobola/Downloads/demo.jpeg",
]


def upload_images():
    for image_path in images:
        if os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
                response = requests.post(UPLOAD_IMAGES_URL, files=files)
                print(response.json())
        else:
            print(f"Error: {image_path} not found.")


def generate_vl_request(texts: list[str], images: list[str], filename: str = "vl_req.json") -> list[dict]:
    messages = [{"type": "text", "text": text} for text in texts]
    messages += [
        {"type": "image", "image": "uploads/" + os.path.basename(img_path)} for img_path in images
    ]

    payload = {"messages": messages}
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"Generated  '{filename}' with {len(texts) + len(images)} requests.")
    return payload


if __name__ == "__main__":
    os.makedirs("responses/", exist_ok=True)

    upload_images()
    _ = generate_vl_request(texts, images)

    request = "vl_req.json"

    with open(request) as f:
        payload = json.load(f)

    response = requests.post(
        f"http://{settings.service_address}:{settings.service_port}/embedding/embed",
        json=payload
    )

    try:
        response_json = json.loads(
            '{"messages":[' + f"{response.text}" + "]}"
        )
    except json.JSONDecodeError as e:
        print(f"Not valid JSON: {e}")

    filename = "response.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(response_json, f, indent=2, ensure_ascii=False)
