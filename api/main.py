from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))

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

handler = Mangum(app)


class SimilarImagesResponse(BaseModel):
    similar_images: List[str]


class SimilarImagesRequest(BaseModel):
    similar_images_names_list: List[str]


@app.get("/")
def index():
    return {"status": "ok"}


@app.post("/search-similar-images", response_model=SimilarImagesResponse)
async def search_similar_images(request: SimilarImagesRequest):
    try:

        # Retrieve similar images from the database
        similar_images_base64 = await get_multiple_images_from_s3_bucket(
            request.similar_images_names_list
        )

        return {"similar_images": similar_images_base64}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
