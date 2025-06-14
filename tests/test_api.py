import pytest
from fastapi.testclient import TestClient
from app.main import app
import os

os.environ["API_TOKEN"] = "test-secret"
# instantiate the TestClient with our FastAPI app
client = TestClient(app)

def test_predict_setosa():
    """Valid input should return Iris-setosa"""
    payload = {
        "sepal_length": 2,
        "sepal_width": 3,
        "petal_length": 2,
        "petal_width": 0.5
    }
    resp = client.post("/predict", json=payload)
    assert resp.status_code == 200
    assert resp.json() == {"species": "Iris-setosa"}

def test_predict_versicolor():
    """Another valid input should return Iris-versicolor"""
    payload = {
        "sepal_length": 4,
        "sepal_width": 3,
        "petal_length": 1,
        "petal_width": 2
    }
    resp = client.post("/predict", json=payload)
    assert resp.status_code == 200
    assert resp.json() == {"species": "Iris-versicolor"}

def test_missing_field():
    """Omitting a required field should give 422"""
    payload = {
        "sepal_length": 4,
        "sepal_width": 3,
        "petal_length": 1
        # petal_width is missing
    }
    resp = client.post("/predict", json=payload)
    assert resp.status_code == 422
    # check that the error mentions the missing field
    assert any(err["loc"][-1] == "petal_width" for err in resp.json()["detail"])

def test_string_numbers_coerced():
    """Numeric values as strings should still work"""
    payload = {
        "sepal_length": "4",
        "sepal_width": 3,
        "petal_length": "1",
        "petal_width": "2"
    }
    resp = client.post("/predict", json=payload)
    assert resp.status_code == 200
    assert resp.json() == {"species": "Iris-setosa"}

def test_invalid_string_errors():
    """Non-numeric strings should produce a 422 type_error.float"""
    payload = {
        "sepal_length": "BIPM",
        "sepal_width": 3,
        "petal_length": "Hallo",
        "petal_width": 2
    }
    resp = client.post("/predict", json=payload)
    assert resp.status_code == 422
    # error for each of the bad fields
    errs = resp.json()["detail"]
    bad_fields = {e["loc"][-1] for e in errs}
    assert "sepal_length" in bad_fields
    assert "petal_length" in bad_fields
