import numpy as np
import lightgbm as lgb
from google.cloud import aiplatform, storage

from settings import GCP_PROJECT_ID, GCP_REGION, TARGET_LABELS, MODEL_TYPE
from src.api.schemas import PredictionRequest


class Predictor:
    def __init__(self):
        self.model = self._load_model_from_registry()

    def _load_model_from_registry(self):
        """
        Queries Model Registry for latest production model,
        downloads from GCS and loads into memory.
        """
        aiplatform.init(project=GCP_PROJECT_ID, location=GCP_REGION)

        # Find latest production model for this model type
        models = aiplatform.Model.list(
            filter=f'labels.stage="production" AND labels.model-type="{MODEL_TYPE}"',
            order_by="create_time desc",
        )

        if not models:
            raise RuntimeError(f"No production model found for model-type={MODEL_TYPE}")

        latest_model = models[0]
        print(f"Loading model: {latest_model.display_name}")
        print(f"Labels: {latest_model.labels}")

        # Get GCS URI of model artifact
        model_uri = latest_model.uri
        print(f"Model URI: {model_uri}")

        # Download model file from GCS to /tmp/
        local_path = "/tmp/model.lgb"
        self._download_from_gcs(model_uri, local_path)

        # Load with LightGBM native format
        booster = lgb.Booster(model_file=local_path)
        print("Model loaded successfully")
        return booster

    def _download_from_gcs(self, gcs_uri: str, local_path: str) -> None:
        """Downloads model artifact from GCS URI to local path."""
        gcs_uri = gcs_uri.rstrip("/") + "/model"
        parts = gcs_uri.replace("gs://", "").split("/")
        bucket_name = parts[0]
        blob_path = "/".join(parts[1:])

        client = storage.Client(project=GCP_PROJECT_ID)
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_path)
        blob.download_to_filename(local_path)
        print(f"Downloaded model from {gcs_uri} to {local_path}")

    def predict(self, pred_request: PredictionRequest):
        """Assemble features, run inference and return prediction."""
        X = np.array(
            pred_request.group1.values +
            pred_request.group2.values +
            pred_request.comparator.values
        ).reshape(1, -1)

        # LightGBM Booster returns probabilities directly
        probabilities = self.model.predict(X)[0]
        prediction = int(np.argmax(probabilities))
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