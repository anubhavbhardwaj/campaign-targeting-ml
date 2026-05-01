from src.data.processor import DataProcessor
from src.model.trainer import ModelTrainer

if __name__ == "__main__":
    processor = DataProcessor()
    trainer = ModelTrainer(processor)
    trainer.train()