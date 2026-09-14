import { useEffect, useState } from 'react';
import { BrowserRouter, Link, NavLink, Route, Routes } from 'react-router-dom';
import './App.css';

const API_BASE = 'http://127.0.0.1:8000';

function StatCard({ title, value, hint, tone = 'blue' }) {
  return (
    <div className="card stat-card">
      <div className={`badge badge-${tone}`}>{title}</div>
      <h3>{value}</h3>
      <p>{hint}</p>
    </div>
  );
}

function RiskPill({ level }) {
  const map = {
    Low: 'low',
    Medium: 'medium',
    High: 'high',
  };

  return <span className={`risk-pill ${map[level] || 'low'}`}>{level}</span>;
}

function OverviewPage() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetch(`${API_BASE}/analytics/overview`)
      .then((res) => res.json())
      .then((data) => setStats(data))
      .catch(() => setStats({
        total_students: 0,
        low_risk: 0,
        medium_risk: 0,
        high_risk: 0,
        dropout_rate: 0,
        average_attendance: 0,
        average_academic_performance: 0,
        students_requiring_attention: 0,
      }));
  }, []);

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <p className="eyebrow">Overview</p>
          <h1>Student Dropout Dashboard</h1>
        </div>
        <Link className="primary-btn" to="/prediction">Predict Risk</Link>
      </div>

      {!stats ? (
        <div className="card empty-state">Loading dashboard...</div>
      ) : (
        <>
          <div className="stats-grid">
            <StatCard title="Total Students" value={stats.total_students} hint="Currently tracked" tone="blue" />
            <StatCard title="Low Risk" value={stats.low_risk} hint="Lower concern" tone="green" />
            <StatCard title="Medium Risk" value={stats.medium_risk} hint="Monitoring needed" tone="amber" />
            <StatCard title="High Risk" value={stats.high_risk} hint="Needs support" tone="red" />
            <StatCard title="Dropout Rate" value={`${stats.dropout_rate}%`} hint="Estimated rate" tone="purple" />
            <StatCard title="Avg Attendance" value={`${stats.average_attendance}%`} hint="Across all students" tone="cyan" />
            <StatCard title="Avg Performance" value={`${stats.average_academic_performance}%`} hint="Academic average" tone="indigo" />
            <StatCard title="Needs Attention" value={stats.students_requiring_attention} hint="Priority cases" tone="rose" />
          </div>

          <div className="card alert-box">
            <strong>Important:</strong> Predictions are estimates based on historical data and should not be used as the sole basis for decisions about a student's education. Human review and appropriate support are required.
          </div>
        </>
      )}
    </div>
  );
}

function StudentsPage() {
  const [students, setStudents] = useState([]);
  const [form, setForm] = useState({
    student_id: '',
    age: 20,
    gender: 'Female',
    course: 'B.Sc. Computer Science',
    semester: 3,
    attendance: 80,
    previous_semester_marks: 75,
    current_internal_marks: 78,
    assignment_score: 80,
    previous_cgpa: 7.2,
    backlogs: 0,
    study_hours: 4,
    academic_performance: 78,
    dropout_label: 0,
  });

  const loadStudents = () => {
    fetch(`${API_BASE}/students`)
      .then((res) => res.json())
      .then((data) => setStudents(data))
      .catch(() => setStudents([]));
  };

  useEffect(() => {
    loadStudents();
  }, []);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const payload = { ...form, age: Number(form.age), semester: Number(form.semester), attendance: Number(form.attendance), previous_semester_marks: Number(form.previous_semester_marks), current_internal_marks: Number(form.current_internal_marks), assignment_score: Number(form.assignment_score), previous_cgpa: Number(form.previous_cgpa), backlogs: Number(form.backlogs), study_hours: Number(form.study_hours), academic_performance: Number(form.academic_performance), dropout_label: Number(form.dropout_label) };

    const res = await fetch(`${API_BASE}/students`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (res.ok) {
      setForm({
        student_id: '',
        age: 20,
        gender: 'Female',
        course: 'B.Sc. Computer Science',
        semester: 3,
        attendance: 80,
        previous_semester_marks: 75,
        current_internal_marks: 78,
        assignment_score: 80,
        previous_cgpa: 7.2,
        backlogs: 0,
        study_hours: 4,
        academic_performance: 78,
        dropout_label: 0,
      });
      loadStudents();
    }
  };

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <p className="eyebrow">Student Management</p>
          <h1>Students</h1>
        </div>
      </div>

      <div className="split-layout">
        <form className="card form-card" onSubmit={handleSubmit}>
          <h3>Add Student</h3>
          <div className="form-grid">
            <label>Student ID<input name="student_id" value={form.student_id} onChange={handleChange} required /></label>
            <label>Age<input name="age" type="number" value={form.age} onChange={handleChange} /></label>
            <label>Gender<select name="gender" value={form.gender} onChange={handleChange}><option>Female</option><option>Male</option><option>Other</option></select></label>
            <label>Course<input name="course" value={form.course} onChange={handleChange} /></label>
            <label>Semester<input name="semester" type="number" value={form.semester} onChange={handleChange} /></label>
            <label>Attendance %<input name="attendance" type="number" value={form.attendance} onChange={handleChange} /></label>
            <label>Previous Marks<input name="previous_semester_marks" type="number" value={form.previous_semester_marks} onChange={handleChange} /></label>
            <label>Internal Marks<input name="current_internal_marks" type="number" value={form.current_internal_marks} onChange={handleChange} /></label>
            <label>Assignment<input name="assignment_score" type="number" value={form.assignment_score} onChange={handleChange} /></label>
            <label>CGPA<input name="previous_cgpa" type="number" step="0.1" value={form.previous_cgpa} onChange={handleChange} /></label>
            <label>Backlogs<input name="backlogs" type="number" value={form.backlogs} onChange={handleChange} /></label>
            <label>Study Hours<input name="study_hours" type="number" step="0.1" value={form.study_hours} onChange={handleChange} /></label>
            <label>Academic Performance<input name="academic_performance" type="number" value={form.academic_performance} onChange={handleChange} /></label>
            <label>Dropout Label<select name="dropout_label" value={form.dropout_label} onChange={handleChange}><option value={0}>0 - Not at risk</option><option value={1}>1 - At risk</option></select></label>
          </div>
          <button type="submit" className="primary-btn">Save Student</button>
        </form>

        <div className="card table-card">
          <h3>Student List</h3>
          <div className="table-scroll">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Course</th>
                  <th>Attendance</th>
                  <th>CGPA</th>
                  <th>Risk</th>
                </tr>
              </thead>
              <tbody>
                {students.length ? students.map((student) => (
                  <tr key={student.id}>
                    <td>{student.student_id}</td>
                    <td>{student.course}</td>
                    <td>{student.attendance}%</td>
                    <td>{student.previous_cgpa}</td>
                    <td><RiskPill level={student.dropout_label === 1 ? 'High' : 'Low'} /></td>
                  </tr>
                )) : (
                  <tr><td colSpan="5">No students available.</td></tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

function PredictionPage() {
  const [form, setForm] = useState({
    student_id: 'STU-NEW',
    age: 20,
    gender: 'Female',
    course: 'B.Sc. Computer Science',
    semester: 3,
    attendance: 72,
    previous_semester_marks: 68,
    current_internal_marks: 70,
    assignment_score: 74,
    previous_cgpa: 6.8,
    backlogs: 1,
    study_hours: 3.5,
    academic_performance: 70,
  });
  const [result, setResult] = useState(null);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const payload = { ...form, age: Number(form.age), semester: Number(form.semester), attendance: Number(form.attendance), previous_semester_marks: Number(form.previous_semester_marks), current_internal_marks: Number(form.current_internal_marks), assignment_score: Number(form.assignment_score), previous_cgpa: Number(form.previous_cgpa), backlogs: Number(form.backlogs), study_hours: Number(form.study_hours), academic_performance: Number(form.academic_performance) };

    const res = await fetch(`${API_BASE}/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    const data = await res.json();
    setResult(data);
  };

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <p className="eyebrow">Prediction</p>
          <h1>Dropout Risk Prediction</h1>
        </div>
      </div>

      <div className="split-layout">
        <form className="card form-card" onSubmit={handleSubmit}>
          <h3>Student Information</h3>
          <div className="form-grid">
            <label>Student ID<input name="student_id" value={form.student_id} onChange={handleChange} /></label>
            <label>Age<input name="age" type="number" value={form.age} onChange={handleChange} /></label>
            <label>Gender<select name="gender" value={form.gender} onChange={handleChange}><option>Female</option><option>Male</option><option>Other</option></select></label>
            <label>Course<input name="course" value={form.course} onChange={handleChange} /></label>
            <label>Semester<input name="semester" type="number" value={form.semester} onChange={handleChange} /></label>
            <label>Attendance %<input name="attendance" type="number" value={form.attendance} onChange={handleChange} /></label>
            <label>Previous Marks<input name="previous_semester_marks" type="number" value={form.previous_semester_marks} onChange={handleChange} /></label>
            <label>Internal Marks<input name="current_internal_marks" type="number" value={form.current_internal_marks} onChange={handleChange} /></label>
            <label>Assignment Score<input name="assignment_score" type="number" value={form.assignment_score} onChange={handleChange} /></label>
            <label>CGPA<input name="previous_cgpa" type="number" step="0.1" value={form.previous_cgpa} onChange={handleChange} /></label>
            <label>Backlogs<input name="backlogs" type="number" value={form.backlogs} onChange={handleChange} /></label>
            <label>Study Hours<input name="study_hours" type="number" step="0.1" value={form.study_hours} onChange={handleChange} /></label>
            <label>Academic Performance<input name="academic_performance" type="number" value={form.academic_performance} onChange={handleChange} /></label>
          </div>
          <button type="submit" className="primary-btn">Predict Dropout Risk</button>
        </form>

        <div className="card result-card">
          {result ? (
            <>
              <h3>Prediction</h3>
              <h2>{result.risk_level}</h2>
              <div className="result-row"><span>Probability</span><strong>{result.probability}%</strong></div>
              <div className="result-row"><span>Prediction</span><strong>{result.prediction}</strong></div>
              <div className="result-row"><span>Risk Level</span><RiskPill level={result.risk_level} /></div>
              <p className="explanation">{result.explanation}</p>
              <div className="feature-box">
                <h4>Important contributing factors</h4>
                <ul>
                  {result.important_features.map((feature) => <li key={feature}>{feature}</li>)}
                </ul>
              </div>
              <p className="note">{result.note}</p>
            </>
          ) : (
            <div className="empty-state">No prediction yet. Fill in student details and click Predict.</div>
          )}
        </div>
      </div>
    </div>
  );
}

function AnalyticsPage() {
  return (
    <div className="page">
      <div className="page-header">
        <div>
          <p className="eyebrow">Analytics</p>
          <h1>Academic and Risk Trends</h1>
        </div>
      </div>
      <div className="card analytics-card">
        <p>This analytics view is designed for demo-level insights. It helps identify patterns related to attendance, academic performance, and dropout risk. Correlation does not prove causation.</p>
      </div>
    </div>
  );
}

function DatasetPage() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');

  const handleUpload = async (event) => {
    event.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    const res = await fetch(`${API_BASE}/dataset/upload`, {
      method: 'POST',
      body: formData,
    });

    const data = await res.json();
    setMessage(res.ok ? `${data.message} Rows: ${data.rows_loaded}` : data.detail || 'Upload failed');
  };

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <p className="eyebrow">Dataset</p>
          <h1>Upload Dataset</h1>
        </div>
      </div>
      <div className="card form-card">
        <form onSubmit={handleUpload}>
          <label className="upload-label">
            Choose CSV file
            <input type="file" accept=".csv" onChange={(e) => setFile(e.target.files[0])} />
          </label>
          <button type="submit" className="primary-btn">Upload CSV</button>
        </form>
        {message && <p className="message-box">{message}</p>}
      </div>
    </div>
  );
}

function ModelPage() {
  const [metrics, setMetrics] = useState(null);

  const trainModel = async () => {
    const res = await fetch(`${API_BASE}/model/train`, { method: 'POST' });
    const data = await res.json();
    setMetrics(data);
  };

  useEffect(() => {
    fetch(`${API_BASE}/model/metrics`)
      .then((res) => res.json())
      .then((data) => setMetrics(data))
      .catch(() => setMetrics(null));
  }, []);

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <p className="eyebrow">Model</p>
          <h1>Machine Learning Model</h1>
        </div>
        <button className="primary-btn" onClick={trainModel}>Train Model</button>
      </div>

      <div className="stats-grid">
        <StatCard title="Accuracy" value={metrics ? `${metrics.accuracy * 100}%` : 'N/A'} hint="Classification accuracy" tone="green" />
        <StatCard title="Precision" value={metrics ? `${metrics.precision * 100}%` : 'N/A'} hint="Positive predictive value" tone="blue" />
        <StatCard title="Recall" value={metrics ? `${metrics.recall * 100}%` : 'N/A'} hint="Ability to catch at-risk cases" tone="red" />
        <StatCard title="F1-score" value={metrics ? `${metrics.f1_score * 100}%` : 'N/A'} hint="Balance of precision and recall" tone="purple" />
        <StatCard title="ROC-AUC" value={metrics ? `${metrics.roc_auc * 100}%` : 'N/A'} hint="Separation power" tone="cyan" />
      </div>
    </div>
  );
}

function AppShell() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <aside className="sidebar">
          <div className="brand">
            <div className="brand-mark">D</div>
            <div>
              <strong>Dropout</strong>
              <small>Analytics</small>
            </div>
          </div>

          <nav className="nav">
            <NavLink to="/" end>Overview</NavLink>
            <NavLink to="/students">Students</NavLink>
            <NavLink to="/prediction">Prediction</NavLink>
            <NavLink to="/analytics">Analytics</NavLink>
            <NavLink to="/dataset">Dataset</NavLink>
            <NavLink to="/model">ML Model</NavLink>
          </nav>

          <div className="sidebar-note">
            <strong>Ethical note</strong>
            <p>Predictions are estimates, not certainties.</p>
          </div>
        </aside>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<OverviewPage />} />
            <Route path="/students" element={<StudentsPage />} />
            <Route path="/prediction" element={<PredictionPage />} />
            <Route path="/analytics" element={<AnalyticsPage />} />
            <Route path="/dataset" element={<DatasetPage />} />
            <Route path="/model" element={<ModelPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default function App() {
  return <AppShell />;
}
