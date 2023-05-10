from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn
import os
import sys
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app")))

from utils.get_objects_from_aws_s3_bucket import get_multiple_images_from_s3_bucket

from mangum import Mangum

app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SimilarImagesResponse(BaseModel):
    similar_images: List[str]


class SimilarImagesRequest(BaseModel):
    similar_images_names_list: List[str]


# Keep track of number of requests per day and limit to 200 requests per day
requests_per_day = 200
requests_per_day_counter = 0
last_request_date = datetime.datetime.now().date()


def check_request_limit():
    global requests_per_day_counter
    global last_request_date

    if requests_per_day_counter >= requests_per_day:
        if last_request_date == datetime.datetime.now().date():
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="You have reached the limit of requests per day. Please try again tomorrow.",
            )
        else:
            requests_per_day_counter = 0
            last_request_date = datetime.datetime.now().date()

    requests_per_day_counter += 1


# API endpoints


@app.get("/", summary="Health check endpoint")
async def index():
    check_request_limit()
    return {"status": "ok"}


@app.post(
    "/search-similar-images",
    response_model=SimilarImagesResponse,
    summary="Search for similar images",
    description="Given a list of image names, returns a list of similar images in base64 format",
)
async def search_similar_images(request: SimilarImagesRequest):
    """
    Retrieve similar images from the database based on the input image names.
    """
    check_request_limit()

    try:
        similar_images_base64 = await get_multiple_images_from_s3_bucket(
            request.similar_images_names_list
        )
        return {"similar_images": similar_images_base64}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


def handler(event, context):
    print("Event:", event)
    return Mangum(app)(event, context)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
