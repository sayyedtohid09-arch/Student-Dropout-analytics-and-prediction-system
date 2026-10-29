from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class StudentBase(BaseModel):
    student_id: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., ge=15, le=40)
    gender: str = Field(..., min_length=1, max_length=20)
    course: str = Field(..., min_length=2, max_length=100)
    semester: int = Field(..., ge=1, le=12)
    attendance: float = Field(..., ge=0, le=100)
    previous_semester_marks: float = Field(..., ge=0, le=100)
    current_internal_marks: float = Field(..., ge=0, le=100)
    assignment_score: float = Field(..., ge=0, le=100)
    previous_cgpa: float = Field(..., ge=0, le=10)
    backlogs: int = Field(..., ge=0, le=30)
    study_hours: float = Field(..., ge=0, le=12)
    academic_performance: float = Field(..., ge=0, le=100)
    dropout_label: int = Field(default=0, ge=0, le=1)


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    age: Optional[int] = Field(default=None, ge=15, le=40)
    gender: Optional[str] = Field(default=None, min_length=1, max_length=20)
    course: Optional[str] = Field(default=None, min_length=2, max_length=100)
    semester: Optional[int] = Field(default=None, ge=1, le=12)
    attendance: Optional[float] = Field(default=None, ge=0, le=100)
    previous_semester_marks: Optional[float] = Field(default=None, ge=0, le=100)
    current_internal_marks: Optional[float] = Field(default=None, ge=0, le=100)
    assignment_score: Optional[float] = Field(default=None, ge=0, le=100)
    previous_cgpa: Optional[float] = Field(default=None, ge=0, le=10)
    backlogs: Optional[int] = Field(default=None, ge=0, le=30)
    study_hours: Optional[float] = Field(default=None, ge=0, le=12)
    academic_performance: Optional[float] = Field(default=None, ge=0, le=100)
    dropout_label: Optional[int] = Field(default=None, ge=0, le=1)


class StudentRead(StudentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PredictionRequest(BaseModel):
    student_id: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., ge=15, le=40)
    gender: str = Field(..., min_length=1, max_length=20)
    course: str = Field(..., min_length=2, max_length=100)
    semester: int = Field(..., ge=1, le=12)
    attendance: float = Field(..., ge=0, le=100)
    previous_semester_marks: float = Field(..., ge=0, le=100)
    current_internal_marks: float = Field(..., ge=0, le=100)
    assignment_score: float = Field(..., ge=0, le=100)
    previous_cgpa: float = Field(..., ge=0, le=10)
    backlogs: int = Field(..., ge=0, le=30)
    study_hours: float = Field(..., ge=0, le=12)
    academic_performance: float = Field(..., ge=0, le=100)


class PredictionResponse(BaseModel):
    risk_level: str
    probability: float
    prediction: str
    explanation: str
    important_features: list[str]
    note: str


class DashboardStats(BaseModel):
    total_students: int
    low_risk: int
    medium_risk: int
    high_risk: int
    dropout_rate: float
    average_attendance: float
    average_academic_performance: float
    students_requiring_attention: int


class MetricsResponse(BaseModel):
    model_name: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    roc_auc: float
    confusion_matrix: list[list[int]]
    selected_by: str


class DatasetUploadResponse(BaseModel):
    message: str
    rows_loaded: int
    columns: list[str]
    student_dropout_percentages: list[dict[str, float | str]]


class CourseRiskStat(BaseModel):
    course: str
    total_students: int
    at_risk_students: int
    dropout_rate: float


class TrendsResponse(BaseModel):
    total_students: int
    course_breakdown: list[CourseRiskStat]
    attendance_by_risk: dict[str, float]
    academic_by_risk: dict[str, float]
    backlogs_by_risk: dict[str, float]

