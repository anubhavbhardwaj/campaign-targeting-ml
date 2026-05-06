from functools import lru_cache
from fastapi import FastAPI, HTTPException

from src.model.predictor import Predictor
from src.api.schemas import PredictionRequest, PredictionResponse

app = FastAPI(title = "Campaign Targeting API")

@lru_cache
def get_predictor() -> Predictor:
    """Lazy loads the predictor instance and caches it for future use"""
    return Predictor()

@app.get("/health")
def get_health():
    """Health check endpoint to verify if the API is running"""
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    """Endpoint to run prediction on the input data and return the results"""
    try:
        result = get_predictor().predict(request)
        return PredictionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))