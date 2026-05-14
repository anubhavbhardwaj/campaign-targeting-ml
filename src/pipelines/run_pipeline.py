from kfp import compiler
from datetime import datetime
from google.cloud import aiplatform
from pipeline import retraining_pipeline
from settings import GCP_PROJECT_ID, GCP_REGION, BQ_DATASET_ID, BQ_TABLE_ID

# Pipeline config
PIPELINE_ROOT = f"gs://{GCP_PROJECT_ID}-pipeline-artifacts/campaign-targeting"
COMPILED_PIPELINE_PATH = "campaign_targeting_pipeline.yaml"
MODEL_DISPLAY_NAME = "campaign-targeting-lgbm"

def compile_pipeline():
    """Compiles pipeline DAG to YAML spec."""
    compiler.Compiler().compile(
        pipeline_func=retraining_pipeline,
        package_path=COMPILED_PIPELINE_PATH,
    )
    print(f"Pipeline compiled to {COMPILED_PIPELINE_PATH}")


def run_pipeline():
    """Submits compiled pipeline to Vertex AI."""
    aiplatform.init(project=GCP_PROJECT_ID, location=GCP_REGION)

    job = aiplatform.PipelineJob(
        display_name="campaign-targeting-retraining",
        template_path=COMPILED_PIPELINE_PATH,
        pipeline_root=PIPELINE_ROOT,
        parameter_values={
            "project_id": GCP_PROJECT_ID,
            "dataset_id": BQ_DATASET_ID,
            "table_id": BQ_TABLE_ID,
            "region": GCP_REGION,
            "model_display_name": MODEL_DISPLAY_NAME,
            "f1_threshold": 0.48,
            "data_version": datetime.now().strftime("%Y-%m")
        },
        enable_caching=False,
    )

    job.submit()
    print(f"Pipeline submitted. Monitor at:")
    print(f"https://console.cloud.google.com/vertex-ai/pipelines?project={GCP_PROJECT_ID}")


if __name__ == "__main__":
    compile_pipeline()
    run_pipeline()