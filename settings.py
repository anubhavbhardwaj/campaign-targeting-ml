from pathlib import Path

# Project Paths
ROOT_DIR = Path(__file__).parent

DATA_DIR = ROOT_DIR / "data"

MODELS_DIR = ROOT_DIR / "models"
MODEL_PATH = MODELS_DIR / "model.pkl"


# Features
TARGET_COLUMN = "target"

POST_CAMPAIGN_FEATURES = ["g1_21", "g2_21", "c_28"]

# Model Parameters
LGBM_PARAMS = {
    "n_estimators": 300,
    "learning_rate": 0.05,
    "num_leaves": 25,
    "min_child_samples": 80,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "reg_alpha": 0.2,
    "reg_lambda": 0.2,
    "min_split_gain": 0.1,
    "class_weight": "balanced",
    "random_state": 42,
    "verbose": -1,
}

# Target Labels
TARGET_LABELS = {
    0: "Neither group profitable — consider not running this campaign",
    1: "Target Group 1 — higher predicted ROI",
    2: "Target Group 2 — higher predicted ROI",
}

# API Endpoint
API_URL = "https://marketing-api-198390148696.europe-west1.run.app"