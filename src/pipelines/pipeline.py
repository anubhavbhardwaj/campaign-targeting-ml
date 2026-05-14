from kfp.v2 import dsl
from components.data_validation import validate_data
from components.train_model import train_model
from components.evaluate_model import evaluate_model
from components.conditional_deploy import conditional_deploy


@dsl.pipeline(
    name="campaign-targeting-retraining",
    description="End to end retraining pipeline for campaign targeting model"
)
def retraining_pipeline(
    project_id: str,
    dataset_id: str,
    table_id: str,
    region: str,
    model_display_name: str,
    f1_threshold: float = 0.48,
):
    validation_step = validate_data(
        project_id=project_id,
        dataset_id=dataset_id,
        table_id=table_id,
    )

    training_step = train_model(
        input_dataset=validation_step.outputs["output_dataset"],
    )

    evaluation_step = evaluate_model(
        input_dataset=validation_step.outputs["output_dataset"],
        model=training_step.outputs["model"],
        f1_threshold=f1_threshold,
    )

    conditional_deploy(
        model=training_step.outputs["model"],
        metrics=evaluation_step.outputs["metrics"],
        project_id=project_id,
        region=region,
        model_display_name=model_display_name,
    )