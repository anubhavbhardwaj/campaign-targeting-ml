from pathlib import Path

# Project Paths
ROOT_DIR = Path(__file__).parent

DATA_DIR = ROOT_DIR / "data"

MODELS_DIR = ROOT_DIR / "models"


# Features
TARGET_COLUMN = "target"

POST_CAMPAIGN_FEATURES = ["g1_21", "g2_21", "c_28"]