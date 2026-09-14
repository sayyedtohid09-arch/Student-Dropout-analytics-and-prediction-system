# Student Dropout Analytics and Prediction System

This project is a beginner-friendly final-year student project that predicts whether a student may be at risk of dropping out based on academic and behavioral factors.

## Project Overview

The system includes:
- A modern React frontend dashboard
- A FastAPI backend
- SQLite database
- Machine learning model training and evaluation
- CSV upload support
- Prediction endpoint and analytics pages
- Explainable-risk output for demo use

> Important: This is a demonstration project and predictions are estimates based on historical data. They should not be the sole basis for academic decisions.

## Folder Structure

```text
student-dropout-analytics-and-prediction-system/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── ml_service.py
│   │   ├── models.py
│   │   └── schemas.py
│   ├── requirements.txt
│   └── student_dropout.db
├── dataset/
│   └── sample_students.csv
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.ts
│   └── ...
├── README.md
└── .gitignore
```

## Tech Stack

- Frontend: React + Vite
- Backend: FastAPI
- ML: scikit-learn, pandas, numpy
- Database: SQLite
- Visualization: Recharts (can be added later)

## Installation

### 1. Backend setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Frontend setup

```bash
cd frontend
npm install
```

## Running the app

### Backend

```bash
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs

### Frontend

```bash
cd frontend
npm run dev
```

Open http://localhost:5173

## Model Training

The model is trained using the sample CSV file in the dataset folder.

## Limitations

- This project uses synthetic demo data
- Predictions are not guaranteed
- Human review is always required

## License

This is a student project for academic use.
