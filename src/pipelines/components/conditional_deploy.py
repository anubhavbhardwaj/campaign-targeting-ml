from kfp.dsl import component, Input, Model, Metrics

@component(
    base_image="python:3.11-slim",
    packages_to_install=[
        "google-cloud-aiplatform==1.152.0",
    ]
)
def conditional_deploy(
    model: Input[Model],
    metrics: Input[Metrics],
    project_id: str,
    region: str,
    model_display_name: str,
) -> None:
    """
    Uploads model to Vertex AI Model Registry only if
    f1_macro meets the threshold logged in metrics.
    """
    from google.cloud import aiplatform

    # Read metrics logged by evaluate_model
    f1_macro = metrics.metadata["f1_macro"]
    deploy_approved = bool(metrics.metadata["deploy_approved"])

    print(f"F1 macro: {f1_macro}")
    print(f"Deploy approved: {deploy_approved}")

    if not deploy_approved:
        print(f"F1 macro {f1_macro} below threshold. Skipping deployment.")
        return

    # Initialise Vertex AI
    aiplatform.init(project=project_id, location=region)

    # Upload model to Model Registry
    model_resource = aiplatform.Model.upload(
        display_name=model_display_name,
        artifact_uri=model.uri.rsplit("/", 1)[0],
        serving_container_image_uri=(
    "europe-docker.pkg.dev/vertex-ai/prediction/lightgbm-cpu.3-3:latest"
    ),
    )

    print(f"Model uploaded: {model_resource.resource_name}")