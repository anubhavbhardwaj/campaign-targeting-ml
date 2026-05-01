import pandas as pd
from settings import DATA_DIR, TARGET_COLUMN, POST_CAMPAIGN_FEATURES

class DataProcessor:
    def __init__(self, data_path=DATA_DIR / "customerGroups.csv"):
        self.data_path = data_path
        self.df = None

    def load_data(self):
        """Load the dataset from the specified path."""
        self.df = pd.read_csv(self.data_path)
        print(f"Data loaded successfully with shape: {self.df.shape}")

    def preprocess_data(self):
        """Preprocess the data by separating features and target variable."""
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        # Separate features and target variable
        X = self.df.drop(columns=[TARGET_COLUMN] + POST_CAMPAIGN_FEATURES)
        y = self.df[TARGET_COLUMN]
        
        return X, y