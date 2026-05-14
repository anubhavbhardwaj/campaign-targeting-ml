import pandas as pd
from google.cloud import bigquery
from settings import DATA_DIR, GCP_PROJECT_ID, BQ_DATASET_ID

TABLE_ID = "features"
FULL_TABLE_ID = f"{GCP_PROJECT_ID}.{BQ_DATASET_ID}.{TABLE_ID}"

def load_csv_to_bigquery(data_path = DATA_DIR / "customerGroups.csv") -> None:
    """
    Batch loads the campaign csv data from data_path to bigquery at FULL_TABLE_ID
    """
    # Create the client
    client = bigquery.Client(project=GCP_PROJECT_ID)

    # Load the csv into a dataframe
    df = pd.read_csv(data_path)
    print (f"Loaded CSV: {df.shape[0]} rows, {df.shape[1]} columns")

    job_config = bigquery.LoadJobConfig(
        write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE,
        autodetect = True
        )
    
    job = client.load_table_from_dataframe(df, FULL_TABLE_ID, job_config=job_config)
    job.result()

    table = client.get_table(FULL_TABLE_ID)
    print(f"Loaded {table.num_rows} rows into {FULL_TABLE_ID}")


if __name__ == "__main__":
    load_csv_to_bigquery()