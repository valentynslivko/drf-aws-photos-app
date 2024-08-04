import requests
import os

BASE_API_GW_URL = os.environ["API_GW_BASE_URL"]


def invoke_image_processing(b64_image: str) -> requests.Response:
    resp = requests.post(
        BASE_API_GW_URL + "/myresource",
        data={"image": b64_image},
        headers={"Content-Type": "application/json", "Accept": "image/png"},
    )
    if resp.status_code == 200:
        return resp.json()
