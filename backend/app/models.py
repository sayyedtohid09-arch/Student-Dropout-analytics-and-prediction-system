from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text

from .database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    course = Column(String, nullable=False)
    semester = Column(Integer, nullable=False)
    attendance = Column(Float, nullable=False)
    previous_semester_marks = Column(Float, nullable=False)
    current_internal_marks = Column(Float, nullable=False)
    assignment_score = Column(Float, nullable=False)
    previous_cgpa = Column(Float, nullable=False)
    backlogs = Column(Integer, nullable=False)
    study_hours = Column(Float, nullable=False)
    academic_performance = Column(Float, nullable=False)
    dropout_label = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class PredictionRecord(Base):
    __tablename__ = "prediction_records"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, nullable=False)
    risk_level = Column(String, nullable=False)
    probability = Column(Float, nullable=False)
    explanation = Column(Text, default="")
    features = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)


class ModelMetadata(Base):
    __tablename__ = "model_metadata"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, nullable=False)
    accuracy = Column(Float, nullable=False)
    precision = Column(Float, nullable=False)
    recall = Column(Float, nullable=False)
    f1_score = Column(Float, nullable=False)
    roc_auc = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text, default="")
