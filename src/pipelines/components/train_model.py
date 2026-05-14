from kfp.dsl import component, Input, Output, Dataset, Model

@component(
    base_image="python:3.11-slim",
    packages_to_install=[
        "lightgbm==4.6.0",
        "scikit-learn==1.8.0",
        "pandas==2.3.3",
        "numpy==2.4.4",
    ]
)
def train_model(
    input_dataset: Input[Dataset],
    model: Output[Model],
) -> None:
    import subprocess
    import subprocess
    subprocess.run(["apt-get", "update", "-y"], check=True, capture_output=True)
    subprocess.run(["apt-get", "install", "-y", "libgomp1"], check=True, capture_output=True)
    """
    Takes the clean CSV artifact as input from the data validatoin component
    trains a LightGBM model and passes the model as an artifact for the next component
    """
    import pandas as pd
    import lightgbm as lgb
    from sklearn.model_selection import cross_val_score, train_test_split
    from sklearn.metrics import classification_report

    # Read dataset artifact from previous step
    df = pd.read_csv(input_dataset.path)
    print(f"Training data shape: {df.shape}")

    # Split features and target
    TARGET = "target"
    X = df.drop(columns=[TARGET])
    y = df[TARGET]

    # Same params as your submission
    LGBM_PARAMS = {
        "n_estimators": 300,
        "learning_rate": 0.05,
        "num_leaves": 25,
        "min_child_samples": 80,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "reg_alpha": 0.2,
        "reg_lambda": 0.2,
        "min_split_gain": 0.1,
        "class_weight": "balanced",
        "random_state": 42,
        "verbose": -1,
    }

    # Cross validate first
    cv_model = lgb.LGBMClassifier(**LGBM_PARAMS)
    scores = cross_val_score(cv_model, X, y, cv=5, scoring="f1_macro", n_jobs=-1)
    print(f"CV F1 macro: {scores.mean():.3f} ± {scores.std():.3f}")


    # Train on full dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    final_model = lgb.LGBMClassifier(**LGBM_PARAMS)
    final_model.fit(X_train, y_train)

    # Evaluate
    y_pred = final_model.predict(X_test)
    print(classification_report(
        y_test, y_pred,
        target_names=["Neither (0)", "Group 1 (1)", "Group 2 (2)"]
    ))
    
    # Save model artifact
    final_model.booster_.save_model(model.path)
    print(f"Model saved to {model.path}")