from io import BytesIO
from uuid import uuid4
from PIL import Image, ImageFile

import base64
import boto3


def image_to_base64(image_loc: str) -> str:
    with open(image_loc, "rb") as img:
        return base64.b64encode(img.read()).decode()


def crop_center_of_image(image: ImageFile):
    """
    NOTE: might break with smaller images
    """
    WIDTH_AFTER = 200
    HEIGHT_AFTER = 200

    width, height = image.size  # Get dimensions

    left = (width - WIDTH_AFTER) / 2
    top = (height - HEIGHT_AFTER) / 2
    right = (width + WIDTH_AFTER) / 2
    bottom = (height + HEIGHT_AFTER) / 2

    return image.crop((left, top, right, bottom))


def crop_image(base64_image: str):
    b64_decoded_img_bytes = base64_image.encode()
    image = Image.open(BytesIO(base64.b64decode(b64_decoded_img_bytes)))
    return crop_center_of_image(image)


def save_processed_img_to_s3(image: Image, s3_client):
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    BUCKET_NAME = "chi-test-task-profile-images"  # set in envs
    object_key = f"{uuid4()}.png"

    s3_client.put_object(
        Bucket=BUCKET_NAME, Key=object_key, Body=buffer, ContentType="image/png"
    )
    file_link = f"https://{BUCKET_NAME}.s3.amazonaws.com/{object_key}"
    return file_link


if __name__ == "__main__":
    s3_client = boto3.client("s3")

    b64_image: str = image_to_base64("test_img.jpg")
    image_link = save_processed_img_to_s3(crop_image(b64_image), s3_client)
    print(image_link)
