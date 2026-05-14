import pytest
import numpy as np

from src.model.predictor import Predictor
from src.api.schemas import PredictionRequest, ComparatorFeatures, GroupFeatures


@pytest.fixture
def predictor():
    return Predictor()

def test_model_load(predictor):
    assert predictor.model is not None, "Model not loaded successfully."

def test_predict_response_structure(predictor):
    # Generate a sample test to validate response structure
    request = PredictionRequest(
        group1=GroupFeatures(values = np.random.randn(20).tolist()),
        group2=GroupFeatures(values = np.random.rand(20).tolist()),
        comparator=ComparatorFeatures(values = np.random.randn(27).tolist())
    )

    prediction_output = predictor.predict(request)

    assert prediction_output is not None, "Prediction output should not be None."
    assert "prediction" in prediction_output, "Prediction output should contain 'prediction'."
    assert "recommendation" in prediction_output, "Prediction output should contain 'recommendation'."
    assert "confidence" in prediction_output, "Prediction output should contain 'confidence'."
    assert "probabilities" in prediction_output, "Prediction output should contain 'probabilities'."

    assert prediction_output["prediction"] in [0, 1, 2], "Prediction should be 0, 1, or 2."
    assert isinstance(prediction_output["recommendation"], str), "'recommendation' should be a string"
    assert 0.0 <= prediction_output["confidence"] <= 1.0, "Confidence should be between 0 and 1."
    assert set(prediction_output["probabilities"].keys()) == {"neither", "group_1", "group_2"}