import argparse
from src.data.processor import DataProcessor
from src.model.trainer import ModelTrainer

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        choices= ["csv", "bigquery"],
        default= "csv",
        help= "Data source for training"
    )
    args = parser.parse_args()

    processor = DataProcessor(source=args.source)
    trainer = ModelTrainer(processor)
    trainer.train()