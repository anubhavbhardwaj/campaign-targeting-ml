import pickle

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

import lightgbm as lgb

from settings import LGBM_PARAMS, MODELS_DIR
from src.data.processor import DataProcessor


class ModelTrainer():
    def __init__(self, processor: DataProcessor, model = None):
        self.processor = processor
        self.model = model or lgb.LGBMClassifier(**LGBM_PARAMS)
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
    
    def _split_data(self, X, y):
        # Split the data into training and testing sets
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, 
                                                                                random_state=42, stratify=y)

    def _fit(self):
        self.model.fit(self.X_train, self.y_train)

    def _evaluate(self):
        y_pred = self.model.predict(self.X_test)
        print("\nClassification Report:")
        print(classification_report(
            self.y_test, y_pred,
            target_names=['Neither (0)', 'Group 1 (1)', 'Group 2 (2)']
        ))

    def _save(self):
        MODEL_PATH = MODELS_DIR / "model.pkl"
        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(self.model, f)
        
        print (f"Model saved to : {MODEL_PATH}")
    
    def train(self):
        self.processor.load_data()
        X, y = self.processor.preprocess_data()
        self._split_data(X, y)
        self._fit()
        self._evaluate()
        self._save()