from fastapi.testclient import TestClient
from app.main import app
import os
import sys

client = TestClient(app)


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
