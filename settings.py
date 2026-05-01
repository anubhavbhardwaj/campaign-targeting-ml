from pathlib import Path

# Project Paths
ROOT_DIR = Path(__file__).parent

DATA_DIR = ROOT_DIR / "data"

MODELS_DIR = ROOT_DIR / "models"


# Features
TARGET_COLUMN = "target"

POST_CAMPAIGN_FEATURES = ["g1_21", "g2_21", "c_28"]

# Model Parameters
LGBM_PARAMS = {
    "n_estimators": 500,
    "learning_rate": 0.03,
    "num_leaves": 63,
    "min_child_samples": 20,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "class_weight": "balanced",
    "random_state": 42,
    "verbose": -1,
}