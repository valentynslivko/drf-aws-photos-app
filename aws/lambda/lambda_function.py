import os
from PIL import Image, ImageFile
from io import BytesIO
import base64
import boto3
from uuid import uuid4
import json
from urllib.parse import unquote


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
    with Image.open(BytesIO(base64.b64decode(b64_decoded_img_bytes))) as image:
        return crop_center_of_image(image)


def save_processed_img_to_s3(image: Image, s3_client):
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    BUCKET_NAME = os.environ["BucketName"]  # set in envs
    object_key = f"{uuid4()}.png"

    s3_client.put_object(
        Bucket=BUCKET_NAME, Key=object_key, Body=buffer, ContentType="image/png"
    )
    file_link = f"https://{BUCKET_NAME}.s3.amazonaws.com/{object_key}"
    return file_link


def lambda_handler(event, context):
    """
    Expects {"image": "base64 image string"}.
    TODO: additional input validation
    Requires 'Lambda proxy integration' set to 'False'
    """
    payload = event["body"]
    if not payload:
        return {
            "isBase64Encoded": False,
            "statusCode": 400,
            "headers": None,
            "body": "Image was not provided",
        }
        # return {"statusCode": 400, "body": "Image was not provided"}

    s3_client = boto3.client("s3")

    b64_image: str = unquote(
        payload.replace("image=", "")
    )  # TODO: validation if image is empty
    image_link = save_processed_img_to_s3(
        crop_image(b64_image), s3_client
    )  # TODO: exception handling
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": None,
        "body": json.dumps({"image": image_link}),
    }

    # return {"statusCode": 200, "body": {"image": image_link}}
