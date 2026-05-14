from kfp.dsl import component, Output, Dataset

@component(
    base_image="python:3.11-slim",
    packages_to_install=[
        "google-cloud-bigquery==3.41.0",
        "google-cloud-bigquery-storage==2.38.0",
        "db-dtypes==1.6.0",
        "pandas==2.3.3",
    ]
)
def validate_data(
    project_id: str,
    dataset_id: str,
    table_id: str,
    output_dataset: Output[Dataset],
) -> None:
    """
    Queries BigQuery, validates schema and class distribution,
    and outputs a clean CSV artifact for the next step.
    """
    import pandas as pd
    from google.cloud import bigquery

    client = bigquery.Client(project=project_id)

    query = f"""
        SELECT * EXCEPT(g1_21, g2_21, c_28)
        FROM `{project_id}.{dataset_id}.{table_id}`
    """
    df = client.query(query).to_dataframe(create_bqstorage_client=False)
    print(f"Loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"Target dtype: {df['target'].dtype}")
    print(f"Target classes: {df['target'].unique()}")

    # Cast to int to avoid nullable Int64 type issues
    df["target"] = df["target"].astype(int)

    # Validation 1 — expected column count
    assert df.shape[1] == 68, f"Expected 68 columns, got {df.shape[1]}"

    # Validation 2 — no nulls in target
    assert df["target"].isnull().sum() == 0, "Nulls found in target column"

    # Validation 3 — class distribution check
    dist = df["target"].value_counts(normalize=True)
    print(f"Class distribution:\n{dist}")
    for cls in [0, 1, 2]:
        assert cls in dist.index, f"Class {cls} missing from data"

    # Pass clean data to next component as artifact
    df.to_csv(output_dataset.path, index=False)
    print(f"Validation passed. Data saved to {output_dataset.path}")