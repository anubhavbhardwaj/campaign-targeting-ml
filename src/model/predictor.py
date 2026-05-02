import pickle
import numpy as np

from settings import MODELS_DIR, TARGET_LABELS
from src.api.schemas import PredictionRequest

class Predictor:
    def __init__(self,model_name="model.pkl"):
        self.model_path = MODELS_DIR / model_name
        self.model = self._load_model()

    def _load_model(self):
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
        with open(self.model_path, "rb") as f:
            return pickle.load(f)

    def predict(self, pred_request: PredictionRequest):
        X = np.array(pred_request.group1.values +    # ← no self.
                 pred_request.group2.values +
                 pred_request.comparator.values).reshape(1, -1)
        
        prediction = int(self.model.predict(X)[0])
        probabilities = self.model.predict_proba(X)[0]
        confidence = float(probabilities[prediction]) 

        return {
            "prediction": prediction,
            "recommendation": TARGET_LABELS[prediction],
            "confidence": confidence,
            "probabilities": {
                "neither": round(float(probabilities[0]), 3),
                "group_1": round(float(probabilities[1]), 3),
                "group_2": round(float(probabilities[2]), 3),
            }
        }
    