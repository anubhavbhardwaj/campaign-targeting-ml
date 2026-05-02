from fastapi import FastAPI, HTTPException

from src.api.schemas import PredictionRequest, PredictionResponse
from src.model.predictor import Predictor

app = FastAPI(title = "Campaign Targeting API")

predictor = Predictor()

@app.get("/health")
def get_health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    try:
        result = predictor.predict(request)
        return PredictionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))