import requests
import json
from src.embedding.schemas import Message
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

image_url = [
    "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg",
]

images = [
    "/home/kirilltobola/Downloads/demo.jpeg",
    "data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAIAAAAlC+aJAAAE9klEQVR4nOza+1NU5R8HcM/OiqJ+vaB8NVNTxsYroBjgmngpIQ0xKQhNhWBYlASZBiSDDCWJgaRY2EEUTUSEgCndZYHZZCkLRLmNDDFiLrPL3QJBEZQys596v3/oDzhzZs7np9ezwx72M8957o/SrH9v3L+hdpwBJ336DTxLuAuv7l8C911qhhNz1HDcIJ+jj30DPjmenztUfAKnls6GO7QHYDe7ADh31lvwYrdHsGKcxENOQOxQmoZeRGFr10LY6PkyXF6YDRe528HrSyfDtkIW7DcYBKstv8PrNv8Eb/xqE5yrDYF1CVb44LeucHBKBP/vR89hydeAnIDYIWjsHVHwTt8BP/5xH3zG/xBssFkNO2vYTsL6K+DvDHlw24A3bNR/D8clfAmndl2EN2Z9AW+Ir4LNbUfgw9rjsORrQE5A7BCqnnWhYHe/El4TJsB7J7INnBFWweP9NPDx1JXwI/cS+PT+ObBn3i/wtQy2n8L9C+DI6CnwZVM3XD+jHdaEb4YlXwNyAmKH8mlgDQraxDJYp5gAn/bTwx+M1MHGikh4sIZzqg7Vh7B/+8dwYBnn9KqJfH7g9q/hB3PYrmY3OsF5wkJ4bshMWPI1ICcgdihfSn+Cgl+8CdYlhMEZydWw2on99OQgFXz7Vc5PzGu1cHlnI5zVEQVvtnjAmUNcW1e7r4G7PMLhnYUusL2zDyz5GpATEDuUV6e/gEKplf33Yq+18PxorgFKXufnSiv3iyYMsf+eouLa4KGBY4hrGuf9AcVc1x47/xnc4rIBLpv0Nmx7h+PVWe9UWPI1ICcgdggT49gGptokwz+YW+BR7SB8ImQMdrYsh7tVHAfio+xh/5VpsMPoa/A7vpzTG43cnz2wQQebijn+tFfxvT+1ox6WfA3ICYgdQsGv3KtxGuB7f87UCzu4+sLNUZvgNzXp8MypnfDuBq5lj+RzvrT8WQ/c6sr1wHIPzpGszQ78dT9zLW5s3grv+3w7LPkakBMQO5T30jlvac1n/x2z1wLfVZ7nN5z+B5q33IYTLnGeExRzE156KhqutDyGG6/Mg5ckcmzxDMiHR2y94AstuXDJ9UWw5GtATkDsEHrvPEDhoPO78OWBDDjv6VH4ptdD2BzjDBe3cr4UsY3r7ME93HtVLGCb+e3QNfjElT44bVkBnH2BZ203Mnm+ZpvSz2f+NydphZyA2CEs9WJfW7eD52IZsQ3wiqYk2HHXANzncwyuXsF5VFn6+/x7z+lweO9OeLGC+0ILtnLv31XNNlndcw92iR+Gjw7wDE7yNSAnIHYImwJvoaAv94RDFyXCltplcNAY+2mDjvuV62I5j1/V8zc8t557SvZ/2MB7crgeuOXDdUKJdxxs48I2GVzOs7ZpK6yw5GtATkDsUK4M5ny9/+orcPtS3ku7EWGFs+v4vkbpeM9nW78BbqvhPQh9Ee8UzWvmPs/h1bxj5zvGZ+5W8aygMKkcXlXKH93X6Q5LvgbkBMQOYXiE/XSeifMWt+RQuEHBdbOPUxG8tp33QCMLeH48N5lr313u92EPA8+hJwXwPkXTMMeQWsV6uNXuLHx9uBZ25LAk/RqQExA7BE3+JBTO6dnZzgzl+6oOHc8v5PDudMpF3n34fxPXrNMq+ZzMqVtg/1HeIbUV/oIbik7CiX/O5/OfcA3QHco93JTnbrDka0BOQOz4JwAA//+asYDdwHZqpgAAAABJRU5ErkJggg==",
    "data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAIAAAAlC+aJAAAE9klEQVR4nOza+1NU5R8HcM/OiqJ+vaB8NVNTxsYroBjgmngpIQ0xKQhNhWBYlASZBiSDDCWJgaRY2EEUTUSEgCndZYHZZCkLRLmNDDFiLrPL3QJBEZQys596v3/oDzhzZs7np9ezwx72M8957o/SrH9v3L+hdpwBJ336DTxLuAuv7l8C911qhhNz1HDcIJ+jj30DPjmenztUfAKnls6GO7QHYDe7ADh31lvwYrdHsGKcxENOQOxQmoZeRGFr10LY6PkyXF6YDRe528HrSyfDtkIW7DcYBKstv8PrNv8Eb/xqE5yrDYF1CVb44LeucHBKBP/vR89hydeAnIDYIWjsHVHwTt8BP/5xH3zG/xBssFkNO2vYTsL6K+DvDHlw24A3bNR/D8clfAmndl2EN2Z9AW+Ir4LNbUfgw9rjsORrQE5A7BCqnnWhYHe/El4TJsB7J7INnBFWweP9NPDx1JXwI/cS+PT+ObBn3i/wtQy2n8L9C+DI6CnwZVM3XD+jHdaEb4YlXwNyAmKH8mlgDQraxDJYp5gAn/bTwx+M1MHGikh4sIZzqg7Vh7B/+8dwYBnn9KqJfH7g9q/hB3PYrmY3OsF5wkJ4bshMWPI1ICcgdihfSn+Cgl+8CdYlhMEZydWw2on99OQgFXz7Vc5PzGu1cHlnI5zVEQVvtnjAmUNcW1e7r4G7PMLhnYUusL2zDyz5GpATEDuUV6e/gEKplf33Yq+18PxorgFKXufnSiv3iyYMsf+eouLa4KGBY4hrGuf9AcVc1x47/xnc4rIBLpv0Nmx7h+PVWe9UWPI1ICcgdggT49gGptokwz+YW+BR7SB8ImQMdrYsh7tVHAfio+xh/5VpsMPoa/A7vpzTG43cnz2wQQebijn+tFfxvT+1ox6WfA3ICYgdQsGv3KtxGuB7f87UCzu4+sLNUZvgNzXp8MypnfDuBq5lj+RzvrT8WQ/c6sr1wHIPzpGszQ78dT9zLW5s3grv+3w7LPkakBMQO5T30jlvac1n/x2z1wLfVZ7nN5z+B5q33IYTLnGeExRzE156KhqutDyGG6/Mg5ckcmzxDMiHR2y94AstuXDJ9UWw5GtATkDsEHrvPEDhoPO78OWBDDjv6VH4ptdD2BzjDBe3cr4UsY3r7ME93HtVLGCb+e3QNfjElT44bVkBnH2BZ203Mnm+ZpvSz2f+NydphZyA2CEs9WJfW7eD52IZsQ3wiqYk2HHXANzncwyuXsF5VFn6+/x7z+lweO9OeLGC+0ILtnLv31XNNlndcw92iR+Gjw7wDE7yNSAnIHYImwJvoaAv94RDFyXCltplcNAY+2mDjvuV62I5j1/V8zc8t557SvZ/2MB7crgeuOXDdUKJdxxs48I2GVzOs7ZpK6yw5GtATkDsUK4M5ny9/+orcPtS3ku7EWGFs+v4vkbpeM9nW78BbqvhPQh9Ee8UzWvmPs/h1bxj5zvGZ+5W8aygMKkcXlXKH93X6Q5LvgbkBMQOYXiE/XSeifMWt+RQuEHBdbOPUxG8tp33QCMLeH48N5lr313u92EPA8+hJwXwPkXTMMeQWsV6uNXuLHx9uBZ25LAk/RqQExA7BE3+JBTO6dnZzgzl+6oOHc8v5PDudMpF3n34fxPXrNMq+ZzMqVtg/1HeIbUV/oIbik7CiX/O5/OfcA3QHco93JTnbrDka0BOQOz4JwAA//+asYDdwHZqpgAAAABJRU5ErkJggg==",
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


def generate_vl_request(texts: list[str], image_url: list[str], images: list[str], filename: str = "vl_req.json") -> list[dict]:
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
        if "base64" in image_str:
            img = image_str
        else:
            img = settings.upload_dir + os.path.basename(image_str)
        messages.append(
            Message(type="image", image=img).model_dump()
        )

    payload = {
        "messages": messages
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"Generated  '{filename}' with {len(texts) + len(images)} requests.")
    return payload


if __name__ == "__main__":
    os.makedirs("responses/", exist_ok=True)

    upload_images()
    _ = generate_vl_request(texts, image_url, images)

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
