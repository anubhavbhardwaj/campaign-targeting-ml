from kfp.dsl import component, Input, Output, Dataset, Model, Metrics

@component(
    base_image="python:3.11-slim",
    packages_to_install=[
        "lightgbm==4.6.0",
        "scikit-learn==1.8.0",
        "pandas==2.3.3",
        "numpy==2.4.4",
    ]
)
def evaluate_model(
    input_dataset: Input[Dataset],
    model: Input[Model],
    metrics: Output[Metrics],
    f1_threshold: float = 0.48,
) -> None:
    
    import subprocess
    subprocess.run(["apt-get", "update", "-y"], check=True, capture_output=True)
    subprocess.run(["apt-get", "install", "-y", "libgomp1"], check=True, capture_output=True)

    """
    Evaluates trained model and logs metrics as Vertex AI artifact.
    Downstream conditional_deploy reads f1_macro from metrics.
    """
    import pandas as pd
    import lightgbm as lgb
    from sklearn.metrics import f1_score, classification_report
    from sklearn.model_selection import train_test_split
    print("Container started — loading data and model")
    # Load data and model
    df = pd.read_csv(input_dataset.path)
    booster = lgb.Booster(model_file=model.path)

    TARGET = "target"
    X = df.drop(columns=[TARGET])
    y = df[TARGET]

    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Predict
    y_pred_proba = booster.predict(X_test)
    y_pred = y_pred_proba.argmax(axis=1)

    # Compute metrics
    f1_macro = f1_score(y_test, y_pred, average="macro")
    f1_class0 = f1_score(y_test, y_pred, average=None)[0]

    print(classification_report(
        y_test, y_pred,
        target_names=["Neither (0)", "Group 1 (1)", "Group 2 (2)"]
    ))

    # Log metrics to Vertex AI — visible in console
    metrics.log_metric("f1_macro", round(f1_macro, 4))
    metrics.log_metric("f1_class0_neither", round(f1_class0, 4))
    metrics.log_metric("f1_threshold", f1_threshold)
    metrics.log_metric("deploy_approved", int(f1_macro >= f1_threshold))

    print(f"F1 macro: {f1_macro:.4f} — threshold: {f1_threshold}")
    print(f"Deploy approved: {f1_macro >= f1_threshold}")