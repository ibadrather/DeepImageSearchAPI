import os
import sys
import pytest
from PIL import Image
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from utils.get_objects_from_aws_s3_bucket import (
    create_image_url_for_s3_lambda_api_gateway,
    get_image_from_s3_bucket,
)


@pytest.fixture
def env_vars():
    load_dotenv()
    return {
        "BASE_S3_LAMBDA_API_GATEWAY_URL": os.environ["BASE_S3_LAMBDA_API_GATEWAY_URL"],
        "BUCKET_NAME_REV_SEARCH_DATABASE_IMAGES": os.environ[
            "BUCKET_NAME_REV_SEARCH_DATABASE_IMAGES"
        ],
    }


def test_lambda_api(env_vars) -> None:
    base_url = env_vars["BASE_S3_LAMBDA_API_GATEWAY_URL"]
    bucket_name = env_vars["BUCKET_NAME_REV_SEARCH_DATABASE_IMAGES"]

    image_path = "000001_jpg.rf.5182495727dae412fdb258232cd8a86a.jpg"

    image_api_url = create_image_url_for_s3_lambda_api_gateway(
        base_url, bucket_name, image_path
    )
    image = get_image_from_s3_bucket(image_api_url)

    assert isinstance(image, Image.Image), "Image object not returned"
