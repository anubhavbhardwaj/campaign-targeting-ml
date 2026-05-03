import requests
import numpy as np
import pandas as pd
import streamlit as st

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from settings import API_URL


st.title("Profitable Customer Group Prediction")

def generate_features():
    return {
        "group1": {"values": np.random.randn(20).tolist()},
        "group2": {"values": np.random.randn(20).tolist()},
        "comparator": {"values": np.random.randn(27).tolist()}
    }

if st.button("Predict Profitable Group"):
    features = generate_features()
    response = requests.post(f"{API_URL}/predict", json=features)
    if response.status_code == 200:
        result = response.json()
        st.success(f"Predicted Profitable Group: {result['recommendation']} with (Confidence: {result['confidence']:.2f})")
        probs = pd.DataFrame({
            "Probability": [
                result['probabilities']['neither'],
                result['probabilities']['group_1'],
                result['probabilities']['group_2'],
            ]
        }, index=["Neither", "Group 1", "Group 2"])

        st.bar_chart(probs)
    else:
        st.error("Prediction failed. Please try again.")