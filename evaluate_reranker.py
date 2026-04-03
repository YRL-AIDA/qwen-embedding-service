from pathlib import Path

import evaluation.utils as evaluate_utils
from src.reranker.schemas import Message
from src.reranker.schemas import RerankRequest
from src.settings import settings



def generate_vl_request() -> list[dict]:
    """Generate a multi-modal request payload containing text, image URLs, and base64-encoded images.

    This function constructs a list of message dictionaries with various types (text, image_url, image)
    for use in testing or evaluating a vision-language model API. It validates local image paths,
    uploads them if necessary, and ensures all data is properly formatted.

    The resulting dictionary follows the schema expected by the embedding API, where each message
    contains type-specific fields such as 'text', 'image_url', or 'image'.

    Returns:
        dict: A dictionary with a single key "messages" mapping to a list of message objects.
              Each message is a dictionary with keys like 'type', 'text', 'image_url', or 'image',
              properly structured for JSON serialization and API consumption.

    Raises:
        FileNotFoundError: If a specified local image file does not exist.
        Exception: If image upload fails or an invalid image path is provided.
    """
    messages = [
        {
            "type": "text",
            "text": "Some text"
        },
        {
            "type": "image_url",
            "image_url": "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg"
        },
        {
            "type": "image_url",
            "image_url": "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg"
        },
        {
            "type": "image",
            "image": "outside_data_test/testIMG1.jpg"
        },
        {
            "type": "image",
            "image": "outside_data_test/testIMG2.jpg"
        },
        {
            "type": "image",
            "image": evaluate_utils.encode_image_base64("outside_data_test/testIMG1.jpg")
        },
        {
            "type": "image/text",
            "image": "outside_data_test/testIMG1.jpg",
            "text": "Soldiers in a plane, actually they are paratrupers."
        }
    ]

    message_list = []
    for message in messages:
        if "image" in message:
            if "data:image/jpeg;base64," not in message["image"]:
                image_path = Path(message["image"])
                if image_path.is_file():
                    evaluate_utils.upload_image(image_path, settings.UPLOAD_URL)
                else:
                    raise Exception(f"Image path {message['image']} doesn't exists.")
        message_list.append(
            Message(
                type=message["type"],
                text=message.get("text", None),
                image_url=message.get("image_url", None),
                image=message.get("image", None)
            )#.model_dump()
        )
    
    return RerankRequest(
        instruction="Retrieve images or text relevant to the user's query.",
        query={"text": "A woman playing with her dog on a beach at sunset."},
        messages=message_list
    ).model_dump()



if __name__ == "__main__":
    # generate request
    request_name = "rerank_request"
    request_path = evaluate_utils.save_request(
        payload=generate_vl_request(), 
        filename=request_name
    )

    # send request
    response_json = evaluate_utils.send_request(
        request_path,
        URL=settings.RERANK_URL
    )

    # save response to json
    evaluate_utils.save_response(response_json, filename="rerank_response")
