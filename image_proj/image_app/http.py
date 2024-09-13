from typing import Literal
import requests
import os

BASE_API_GW_URL = os.environ["API_GW_BASE_URL"]


def invoke_image_processing(
    b64_image: str,
) -> dict[Literal["status"] | Literal["body"], dict]:
    resp = requests.post(
        BASE_API_GW_URL + "/image",
        data={"image": b64_image},
        headers={"Content-Type": "application/json", "Accept": "image/png"},
    )
    if resp.status_code == 200:
        return {"status": resp.status_code, "body": resp.json()}

    return {"status": resp.status_code, "body": resp.json()}
