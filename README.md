

# Deep Image Search API
This FastAPI-based API provides a simple and efficient way to search for similar images using the DeepSearchLite library. The API receives an image and returns a list of similar images based on a trained feature extractor model. This API serves as the backend for the portfolio web app for the RevImageSearch project, which can be accessed at [My Portfolio](https://ibadrather-appfolio-main-zx8dt2.streamlit.app/).

## Setup
1. Install required packages:
    ```
    pip install fastapi uvicorn Pillow
    ```
2. Download the trained feature extractor model and place it in a models directory.

3. Configure the **MODEL_PATH**, **IMAGES_DIR**, **METADATA_DIR**, and **FEATURE_EXTRACTOR_NAME** variables according to your setup.

4. Run the API:

    ```
    uvicorn backend:app --host 0.0.0.0 --port 8000
    ```

## Usage
Send a POST request to the `/search-similar-images` endpoint with an image file and an optional number of similar images to return.
Example:
```perl
curl -X POST "http://localhost:8000/search-similar-images" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "image=@path_to_image.jpg;type=image/jpeg" -F "number_of_images=3"

```
The API will return a JSON response containing a list of similar images in base64 format:
```json
{
  "similar_images": [
    "data:image/jpeg;base64,...",
    "data:image/jpeg;base64,...",
    "data:image/jpeg;base64,..."
  ]
}

```
You can easily visualize the base64 images in web applications or convert them back to image files using various libraries.

------------------
