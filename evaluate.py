import evaluation.utils as evaluate_utils



def get_text_data():
    """Return a list of textual elements.

    Returns:
        list of str: A list containing text strings.
    """
    return [
        "Some textual request",
    ]


def get_image_urls():
    """Return a list of image urls.

    Returns:
        list of str: A list containing valid image urls.
    """
    return [
        "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg",
        "https://qianwen-res.oss-cn-beijingsdfsd.aliyuncs.com/Qwen-VL/assets/demo.jpeg",
    ]


def get_images():
    """Return a list of image pahts or their Base64-encoded representations.

    This function returns a predefined list containing file paths to two test images
    and their corresponding Base64-encoded strings. It is intended for use in testing
    or evaluation scenarios where both raw file paths and encoded image data are needed.

    Returns:
        list: A list containing strings representing image file paths
              strings representing Base64-encoded image data.
    """
    return [
        "outside_data_test/testIMG1.jpg",
        "outside_data_test/testIMG2.jpg",
        evaluate_utils.encode_image_base64("outside_data_test/testIMG1.jpg"),
    ]



if __name__ == "__main__":
    # generate request
    request_name = "test_request"
    payload = evaluate_utils.generate_vl_request(
        texts=get_text_data(), image_url=get_image_urls(), images=get_images()
    )
    request_path = evaluate_utils.save_request(payload, request_name)

    # send request
    response_json = evaluate_utils.send_request(request_path)

    # save response to json
    evaluate_utils.save_response(response_json, filename="test_response")

    # calculate similarity matrix
    evaluate_utils.calculate_similarity(response_json)
