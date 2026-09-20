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

## Deploying with Supabase and Vercel

The recommended production setup is:

- Vercel for the React/Vite frontend
- Render or Railway for the FastAPI backend
- Supabase PostgreSQL for persistent application data

### Supabase setup

1. Create a Supabase project.
2. Open **Connect** and copy a PostgreSQL connection string. Use the session pooler connection if your backend host cannot use IPv6.
3. Keep the password private. It must only be added to the backend host as `DATABASE_URL`.

The backend supports Supabase through the `DATABASE_URL` environment variable and continues to use SQLite locally when that variable is absent. See `backend/.env.example`.

### Backend deployment

Deploy the `backend` directory to Render or Railway with:

```text
Build command: pip install -r requirements.txt
Start command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Add these backend environment variables:

```text
DATABASE_URL=your Supabase PostgreSQL connection string
FRONTEND_URL=https://your-project.vercel.app
```

After deployment, verify `https://your-backend-host/` and `/docs` load successfully.

### Vercel deployment

1. Import the repository into Vercel.
2. Set **Root Directory** to `frontend`.
3. Set **Build Command** to `npm run build`.
4. Set **Output Directory** to `dist`.
5. Add `VITE_API_BASE_URL` with the public URL of the deployed FastAPI backend.
6. Deploy, then update the backend `FRONTEND_URL` with the final Vercel URL if it changed.

The frontend reads `VITE_API_BASE_URL` at build time. Do not put `DATABASE_URL` or any Supabase service-role key in Vercel frontend variables.

CSV uploads are validated by the backend but are stored on the backend filesystem temporarily. The current model is trained from the repository dataset; persistent file storage and background model training should be added separately before using real data.

## Model Training

The model is trained using the sample CSV file in the dataset folder.

## Limitations

- This project uses synthetic demo data
- Predictions are not guaranteed
- Human review is always required

## License

This is a student project for academic use.
