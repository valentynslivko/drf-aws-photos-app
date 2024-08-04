import base64
import requests
from io import BytesIO


def image_to_base64(image_loc: str) -> str:
    with open(image_loc, "rb") as img:
        return base64.b64encode(img.read()).decode()


def download_image(src: str) -> str:
    file_ext = src.split(".")[-1]
    if file_ext not in ["png", "jpg", "jpeg", "webp"]:
        return
    response = requests.get(src, stream=True)

    response.raise_for_status()
    with BytesIO(response.content) as img:
        b64_image = base64.b64encode(img.read()).decode()

    return b64_image
