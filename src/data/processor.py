import pandas as pd
from google.cloud import bigquery
from settings import (DATA_DIR, TARGET_COLUMN, POST_CAMPAIGN_FEATURES,
                      GCP_PROJECT_ID, BQ_DATASET_ID, BQ_TABLE_ID)

class DataProcessor:
    def __init__(self, data_path=DATA_DIR / "customerGroups.csv", source="csv"):
        self.data_path = data_path
        self.source = source
        self.df = None

    def load_data(self):
        """Load the dataset from the specified path."""
        if self.source == "bigquery":
            self._load_data_from_bigquery()
        else:
            self._load_data_from_csv()

    
    def _load_data_from_csv(self):
        self.df = pd.read_csv(self.data_path)
        print (f"Data Loaded from CSV: {self.df.shape}")
    
    def _load_data_from_bigquery(self):
        client = bigquery.Client(project=GCP_PROJECT_ID)
        query = f"""
            SELECT * EXCEPT({', '.join(POST_CAMPAIGN_FEATURES)})
            FROM `{GCP_PROJECT_ID}.{BQ_DATASET_ID}.{BQ_TABLE_ID}`
        """
        self.df = client.query(query).to_dataframe()
        print(f"Data loaded from BigQuery: {self.df.shape}")


    def preprocess_data(self):
        """Preprocess the data by separating features and target variable."""
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        # Separate features and target variable
        X = self.df.drop(columns=[TARGET_COLUMN] + POST_CAMPAIGN_FEATURES, errors="ignore")
        y = self.df[TARGET_COLUMN]
        
        return X, y