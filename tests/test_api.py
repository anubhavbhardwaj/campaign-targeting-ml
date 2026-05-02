import numpy as np
from fastapi.testclient import TestClient

from src.api.app import app
from src.api.schemas import PredictionRequest, GroupFeatures, ComparatorFeatures

client = TestClient(app)

def test_health():
    assert client.get('/health').status_code == 200, "Health status not correct!"

def test_predict_with_valid_input():
    request = PredictionRequest(
        group1=GroupFeatures(values = np.random.randn(20).tolist()),
        group2=GroupFeatures(values = np.random.rand(20).tolist()),
        comparator=ComparatorFeatures(values = np.random.randn(27).tolist())
    )
    response = client.post('/predict', json=request.model_dump())
    assert response.status_code == 200

def test_predict_with_invalid_input():
    invalid_payload = {
        "group1": {"values": [0.1] * 19},   # ← 19 instead of 20
        "group2": {"values": [0.1] * 20},
        "comparator": {"values": [0.1] * 27}
    }
    response = client.post('/predict', json=invalid_payload)
    assert response.status_code == 422