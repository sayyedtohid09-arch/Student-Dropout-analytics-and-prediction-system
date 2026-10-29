import json
import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import List, Optional

import pandas as pd
from fastapi import Depends, FastAPI, File, Header, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from .database import SessionLocal, engine
from .ml_service import FEATURE_COLUMNS, load_model, predict_dropout_risk, train_and_evaluate_model
from .models import Base, ModelMetadata, PredictionRecord, Student
from .schemas import (
    DatasetUploadResponse,
    MetricsResponse,
    PredictionRequest,
    PredictionResponse,
    StudentCreate,
    StudentRead,
    StudentUpdate,
)

logger = logging.getLogger(__name__)
MAX_UPLOAD_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", str(5 * 1024 * 1024)))


def _resolve_db_path():
    # Kept for documentation; database.py owns engine creation.
    return os.getenv("DATABASE_URL", "sqlite:///./student_dropout.db")


def verify_api_key(x_api_key: Optional[str] = Header(default=None)):
    expected = os.getenv("API_KEY")
    if expected and x_api_key != expected:
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")
    return True

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Train the demo model on startup, but never crash the app if it fails.
    dataset_path = Path(__file__).resolve().parents[2] / "dataset" / "sample_students.csv"
    if dataset_path.exists():
        try:
            df = pd.read_csv(dataset_path)
            metrics = train_and_evaluate_model(df)
            db = SessionLocal()
            try:
                if not db.query(ModelMetadata).first():
                    db.add(ModelMetadata(
                        model_name=metrics["model_name"],
                        accuracy=metrics["accuracy"],
                        precision=metrics["precision"],
                        recall=metrics["recall"],
                        f1_score=metrics["f1_score"],
                        roc_auc=metrics["roc_auc"],
                        confusion_matrix=json.dumps(metrics.get("confusion_matrix")),
                        notes="Model trained on synthetic demo dataset. Results are for educational demonstration purposes only.",
                    ))
                    db.commit()
            finally:
                db.close()
        except Exception as exc:  # pragma: no cover - defensive
            logger.exception("Demo model training failed: %s", exc)
    yield


app = FastAPI(title="Student Dropout Analytics and Prediction System", lifespan=lifespan)

frontend_urls = os.getenv("FRONTEND_URL", "http://localhost:5173")
allowed_origins = [url.strip() for url in frontend_urls.split(",") if url.strip()]
if not allowed_origins:
    allowed_origins = ["http://localhost:5173"]
allow_credentials = "*" not in allowed_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Student Dropout Analytics and Prediction System API is running."}


@app.get("/health")
def health():
    db_ok = True
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
    except Exception:
        db_ok = False
    model_ok = (Path(__file__).resolve().parent.parent / "ml" / "saved_model.joblib").exists()
    return {"status": "ok" if db_ok else "degraded", "database": db_ok, "model": model_ok}


@app.get("/students", response_model=List[StudentRead])
def get_students():
    db = SessionLocal()
    try:
        students = db.query(Student).all()
        return students
    finally:
        db.close()


@app.post("/students", response_model=StudentRead, dependencies=[Depends(verify_api_key)])
def create_student(student: StudentCreate):
    db = SessionLocal()
    try:
        existing = db.query(Student).filter(Student.student_id == student.student_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Student with this ID already exists")

        db_student = Student(**student.model_dump())
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student
    finally:
        db.close()


@app.get("/students/{student_id}", response_model=StudentRead)
def get_student(student_id: int):
    db = SessionLocal()
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student
    finally:
        db.close()


@app.put("/students/{student_id}", response_model=StudentRead, dependencies=[Depends(verify_api_key)])
def update_student(student_id: int, payload: StudentUpdate):
    db = SessionLocal()
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                setattr(student, key, value)

        db.commit()
        db.refresh(student)
        return student
    finally:
        db.close()


@app.delete("/students/{student_id}", dependencies=[Depends(verify_api_key)])
def delete_student(student_id: int):
    db = SessionLocal()
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        db.delete(student)
        db.commit()
        return {"message": "Student deleted successfully"}
    finally:
        db.close()


@app.post("/predict", response_model=PredictionResponse)
def predict_student(payload: PredictionRequest):
    db = SessionLocal()
    try:
        try:
            load_model()
        except FileNotFoundError:
            dataset_path = Path(__file__).resolve().parents[2] / "dataset" / "sample_students.csv"
            if dataset_path.exists():
                df = pd.read_csv(dataset_path)
                train_and_evaluate_model(df)
        result = predict_dropout_risk(payload.model_dump())
        record = PredictionRecord(
            student_id=payload.student_id,
            risk_level=result["risk_level"],
            probability=result["probability"],
            explanation=result["explanation"],
            features=",".join(result["important_features"]),
        )
        db.add(record)
        db.commit()
        return PredictionResponse(**result)
    finally:
        db.close()


@app.post("/dataset/upload", response_model=DatasetUploadResponse, dependencies=[Depends(verify_api_key)])
async def upload_dataset(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

    content = await file.read(MAX_UPLOAD_SIZE + 1)
    if len(content) > MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=413, detail="Uploaded file is too large.")
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    safe_name = Path(file.filename).name
    if not safe_name.lower().endswith(".csv") or "/" in safe_name or "\\" in safe_name:
        raise HTTPException(status_code=400, detail="Invalid file name.")
    upload_dir = Path(__file__).resolve().parent.parent / "dataset"
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / f"uploaded_{safe_name}"

    file_path.write_bytes(content)

    try:
        df = pd.read_csv(file_path)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid CSV file.") from None

    required = [
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
        "dropout_label",
    ]

    missing = [col for col in required if col not in df.columns]
    if missing:
        raise HTTPException(status_code=400, detail=f"CSV is missing required columns: {missing}")

    try:
        model = load_model()
        dropout_percentages = model.predict_proba(df[FEATURE_COLUMNS])[:, 1] * 100
    except Exception:
        raise HTTPException(status_code=500, detail="Could not calculate dropout percentages.") from None

    student_dropout_percentages = [
        {
            "student_id": str(row.get("student_id", f"Student {index + 1}")),
            "dropout_percentage": round(float(dropout_percentages[index]), 2),
        }
        for index, (_, row) in enumerate(df.iterrows())
    ]

    return DatasetUploadResponse(
        message="Dataset uploaded successfully.",
        rows_loaded=len(df),
        columns=df.columns.tolist(),
        student_dropout_percentages=student_dropout_percentages,
    )


@app.get("/analytics/overview")
def analytics_overview():
    db = SessionLocal()
    try:
        students = db.query(Student).all()
        total = len(students)
        if total == 0:
            return {
                "total_students": 0,
                "low_risk": 0,
                "medium_risk": 0,
                "high_risk": 0,
                "dropout_rate": 0,
                "average_attendance": 0,
                "average_academic_performance": 0,
                "students_requiring_attention": 0,
            }

        # Prefer model-based risk bucketing so "medium risk" is meaningful.
        low = high = medium = 0
        try:
            import pandas as pd
            from .ml_service import FEATURE_COLUMNS, load_model

            model = load_model()
            rows = []
            for s in students:
                rows.append({
                    "age": s.age,
                    "gender": s.gender,
                    "course": s.course,
                    "semester": s.semester,
                    "attendance": s.attendance,
                    "previous_semester_marks": s.previous_semester_marks,
                    "current_internal_marks": s.current_internal_marks,
                    "assignment_score": s.assignment_score,
                    "previous_cgpa": s.previous_cgpa,
                    "backlogs": s.backlogs,
                    "study_hours": s.study_hours,
                    "academic_performance": s.academic_performance,
                })
            features = pd.DataFrame(rows)[FEATURE_COLUMNS]
            probs = model.predict_proba(features)[:, 1]
            for prob in probs:
                if prob >= 0.7:
                    high += 1
                elif prob >= 0.4:
                    medium += 1
                else:
                    low += 1
        except Exception:
            low = sum(1 for s in students if s.dropout_label == 0)
            high = sum(1 for s in students if s.dropout_label == 1)
            medium = 0

        return {
            "total_students": total,
            "low_risk": low,
            "medium_risk": medium,
            "high_risk": high,
            "dropout_rate": round((high / total * 100) if total else 0, 2),
            "average_attendance": round(sum(s.attendance for s in students) / total, 2),
            "average_academic_performance": round(sum(s.academic_performance for s in students) / total, 2),
            "students_requiring_attention": high,
        }
    finally:
        db.close()


@app.get("/model/metrics", response_model=MetricsResponse)
def model_metrics():
    db = SessionLocal()
    try:
        metadata = db.query(ModelMetadata).order_by(ModelMetadata.created_at.desc()).first()
        if not metadata:
            raise HTTPException(status_code=404, detail="No model metrics available. Please train the model first.")

        try:
            cm = json.loads(metadata.confusion_matrix or "[]")
        except Exception:
            cm = [[0, 0], [0, 0]]
        if not cm:
            cm = [[0, 0], [0, 0]]

        return MetricsResponse(
            model_name=metadata.model_name,
            accuracy=metadata.accuracy,
            precision=metadata.precision,
            recall=metadata.recall,
            f1_score=metadata.f1_score,
            roc_auc=metadata.roc_auc,
            confusion_matrix=cm,
            selected_by="Cross-validation and test performance",
        )
    finally:
        db.close()


@app.post("/model/train", dependencies=[Depends(verify_api_key)])
def train_model():
    dataset_path = Path(__file__).resolve().parents[2] / "dataset" / "sample_students.csv"
    if not dataset_path.exists():
        raise HTTPException(status_code=404, detail="Dataset not found. Upload or generate a sample CSV first.")

    df = pd.read_csv(dataset_path)
    metrics = train_and_evaluate_model(df)

    db = SessionLocal()
    try:
        record = ModelMetadata(
            model_name=metrics["model_name"],
            accuracy=metrics["accuracy"],
            precision=metrics["precision"],
            recall=metrics["recall"],
            f1_score=metrics["f1_score"],
            roc_auc=metrics["roc_auc"],
            confusion_matrix=json.dumps(metrics.get("confusion_matrix")),
            notes="Model trained on synthetic demo dataset. Results are for educational demonstration purposes only.",
        )
        db.add(record)
        db.commit()
    finally:
        db.close()

    return {"message": "Model trained successfully.", **metrics}
