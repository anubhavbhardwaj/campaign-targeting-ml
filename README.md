# Campaign Targeting ML

## Goal of the Project
In this exercise we are given historical data of marketing campaigns a retail company ran and the outcome of each of the campaign, whether Group(1) gave a better ROI, or Group (2) gave a better ROI, or Neither of them. The task is the first create a Machine Learning Model that can predict which of the Groups, if any, will give a better ROI for the campaign, productionalizing this solution in the cloud to provide an API interface for the model usage and a frontend application for business interaction of the solution. 

## Project Structure
```text
├── Dockerfile
├── README.md
├── cloudbuild-frontend.yaml
├── cloudbuild.yaml
├── data
│   └── customerGroups.csv
├── frontend
│   ├── Dockerfile
│   └── app.py
├── models
│   └── model.pkl
├── notebooks
│   ├── eda.ipynb
│   └── modelling.ipynb
├── pyproject.toml
├── requirements-frontend.txt
├── requirements.txt
├── settings.py
├── src
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── app.py
│   │   └── schemas.py
│   ├── data
│   │   ├── __init__.py
│   │   └── processor.py
│   └── model
│       ├── __init__.py
│       ├── predictor.py
│       └── trainer.py
├── tests
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_predictor.py
│   └── test_processor.py
└── train.py
```


## Important Model Notes
1. Features g1_21, g2_21, and c_28 are post campaign feature and are excluded from training.
2. No major feature engineeing is done, but variance check of variables revaled c_27 has near zero variance. 
3. Relatively less attention was given to Model improvement and I chose LightGBM to have realiable explainations using SHAP for business understanding. 

## Running the API locally
1. In the terminal, first create a virtual environment, activate it, and install the requirements.
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -r requirements.txt
```

2. Train the Model
```bash
python train.py
```

3. Run the API locally using uvicorn
```bash
uvicorn src.api.app:app --host 0.0.0.0 --port 8080
```


## Running the frontend(Streamlit) app locally
1. Install dependencies
```bash
pip install -r requirements-frontend.txt
```

2. Run the Streamlit app
```bash
streamlit run frontend/app.py
```

The frontend will open at http://localhost:8501

Make sure to run API before running the streamlit app. Update the settings 'API_URL' to point to the right API endpoint. 

## Running tests
```bash
pytest tests/ -v
```

## API Endpoints

### Health Check
**GET** `/health`

Response:
```json
{
  "status": "ok"
}
```

### Predict
**POST** `/predict`

Body:
```json
{
    "group1": {"values": [20 floats]},
    "group2": {"values": [20 floats]},
    "comparator": {"values": [27 floats]}
}
```
Returns:
```
{
  "prediction": <str>,
  "recommendation": <str>,
  "confidence": <float>,
  "probabilities": : <dict(str:float)>
}
```

## Live Endpoints
API:      https://marketing-api-198390148696.europe-west1.run.app

Frontend: https://campaign-targeting-frontend-198390148696.europe-west1.run.app


## Production Notes
- In production, features are computed via a dbt transformation stored in Vertex AI feature Store or Bigquery
- Model training runs on Vertex AI custom Training Job
- Model artifact stored in Vertex AI Model Registry
- Model monitoring happens via Vertex Model Monitoring
- Retraining is scheduled using Cloud Schedular and triggered by Vertex AI Model Monitoring drift alerts
- Infrastructure is managed via terraform
- CI/CD via Cloud Build triggers on push to main