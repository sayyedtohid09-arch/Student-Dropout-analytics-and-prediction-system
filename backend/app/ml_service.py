import os
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

FEATURE_COLUMNS = [
    "age",
    "gender",
    "course",
    "semester",
    "attendance",
    "previous_semester_marks",
    "current_internal_marks",
    "assignment_score",
    "previous_cgpa",
    "backlogs",
    "study_hours",
    "academic_performance",
]
TARGET_COLUMN = "dropout_label"
MODEL_PATH = Path(__file__).resolve().parent.parent / "ml" / "saved_model.joblib"


def _get_feature_types(df: pd.DataFrame):
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = [col for col in df.columns if col not in numeric_cols]
    numeric_features = [c for c in FEATURE_COLUMNS if c in numeric_cols]
    categorical_features = [c for c in FEATURE_COLUMNS if c in categorical_cols]
    return numeric_features, categorical_features


def build_model_pipeline(df: pd.DataFrame):
    numeric_features, categorical_features = _get_feature_types(df)

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", Pipeline([("imputer", SimpleImputer(strategy="median"))]), numeric_features),
            (
                "cat",
                Pipeline([
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("onehot", OneHotEncoder(handle_unknown="ignore")),
                ]),
                categorical_features,
            ),
        ]
    )

    model = RandomForestClassifier(
        n_estimators=250,
        max_depth=8,
        random_state=42,
        class_weight="balanced",
    )

    pipeline = Pipeline([("preprocessor", preprocessor), ("model", model)])
    return pipeline


def train_and_evaluate_model(df: pd.DataFrame):
    required = FEATURE_COLUMNS + [TARGET_COLUMN]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")

    df = df.copy()
    df[TARGET_COLUMN] = df[TARGET_COLUMN].astype(int)

    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    pipeline = build_model_pipeline(pd.concat([X_train, y_train], axis=1))
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "model_name": "RandomForestClassifier",
        "accuracy": round(float(accuracy_score(y_test, y_pred)), 4),
        "precision": round(float(precision_score(y_test, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, y_pred, zero_division=0)), 4),
        "f1_score": round(float(f1_score(y_test, y_pred, zero_division=0)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, y_prob)), 4),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
    }

    os.makedirs(MODEL_PATH.parent, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    return metrics


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Model has not been trained yet. Please train the model first.")
    return joblib.load(MODEL_PATH)


def predict_dropout_risk(payload: dict):
    model = load_model()
    df = pd.DataFrame([payload])
    prob = float(model.predict_proba(df[FEATURE_COLUMNS])[0, 1])
    pred = int(prob >= 0.5)

    if prob >= 0.7:
        risk_level = "High"
    elif prob >= 0.4:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    explanation = (
        "This prediction uses patterns learned from the training dataset. The model pays particular attention to "
        "attendance, academic performance, previous CGPA, and backlog information."
    )
    important_features = [
        "attendance",
        "previous_cgpa",
        "backlogs",
        "current_internal_marks",
    ]

    return {
        "risk_level": risk_level,
        "probability": round(prob * 100, 2),
        "prediction": "Dropout Risk" if pred == 1 else "No Dropout Risk",
        "explanation": explanation,
        "important_features": important_features,
        "note": "Predictions are estimates based on historical data and should not be used as the sole basis for decisions about a student's education. Human review and appropriate support are required.",
    }
