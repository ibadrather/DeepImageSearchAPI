# Reverse Image Search API Documentation

## Overview

This API provides endpoints to search for similar images using a list of image names. It returns the similar images in base64 format. There is a limit of 200 requests per day.

## Base URL

```arduino
https://ibadrather-appfolio-main-zx8dt2.streamlit.app/
```
## Authentication

No authentication is required for this API.

## CORS

CORS is configured to allow all origins, methods, and headers.

## Endpoints

### 1. Health Check
* **URL**: /
* **Method**: GET
* **Description**: This endpoint checks the health of the API and verifies that it is up and running.

#### Response

* **Status Code**: 200 OK
* **Content**: { "status": "ok" }

### 2. Search Similar Images
* **URL**: /search-similar-images
* **Method**: POST
* **Description**: Given a list of image names, this endpoint returns a list of similar images in base64 format.

#### Request

* **Content-Type**: application/json
* **Body**:
    ```json
    {
    "similar_images_names_list": ["image1.jpg", "image2.jpg"]
    }
    ```

#### Response

* Status Codes:
  * **200 OK**: Similar images were found and are being returned.
  * **400 BAD REQUEST**: An error occurred while processing the request.
  * **429 TOO MANY REQUESTS**: The limit of 200 requests per day has been reached.

* **Content-Type**: application/json
* **Body**:
    ```json
    {
    "similar_images": ["base64_image1", "base64_image2"]
    }
    ```
## Errors

In case of an error, the API returns an HTTPException with the corresponding status code and a descriptive error message.

Example:

```json
{
  "detail": "Error message"
}
```

## Rate Limiting

The API has a limit of 200 requests per day. If the limit is reached, an **`HTTPException`** with status code **`429 TOO MANY REQUESTS`** is raised. To reset the counter, wait until the next day.

## Python Client Example

Here's an example of how to call the **/search-similar-images** endpoint using Python and the requests library:

```python
import requests

url = "https://your-api-domain.com/search-similar-images"
data = {
  "similar_images_names_list": ["image1.jpg", "image2.jpg"]
}

response = requests.post(url, json=data)

if response.status_code == 200:
    similar_images = response.json()["similar_images"]
    print("Similar images:", similar_images)
else:
    print("Error:", response.json()["detail"])
```

------------------
