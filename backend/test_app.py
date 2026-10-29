import pytest
from fastapi.testclient import TestClient
from uuid import uuid4

from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def test_root_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'message' in response.json()


def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200
    body = response.json()
    assert 'status' in body
    assert 'database' in body
    assert 'model' in body


def test_student_creation_and_fetch(client):
    payload = {
        'student_id': f'TEST-{uuid4().hex[:8]}',
        'age': 20,
        'gender': 'Female',
        'course': 'B.Sc. Computer Science',
        'semester': 3,
        'attendance': 85,
        'previous_semester_marks': 78,
        'current_internal_marks': 80,
        'assignment_score': 82,
        'previous_cgpa': 7.8,
        'backlogs': 0,
        'study_hours': 4.7,
        'academic_performance': 81,
        'dropout_label': 0,
    }

    create_response = client.post('/students', json=payload)
    assert create_response.status_code == 200
    student = create_response.json()
    assert student['student_id'] == payload['student_id']

    fetch_response = client.get('/students')
    assert fetch_response.status_code == 200
    assert any(item['student_id'] == payload['student_id'] for item in fetch_response.json())


def test_prediction_endpoint(client):
    payload = {
        'student_id': 'PRED-001',
        'age': 19,
        'gender': 'Male',
        'course': 'B.Sc. Computer Science',
        'semester': 2,
        'attendance': 60,
        'previous_semester_marks': 58,
        'current_internal_marks': 62,
        'assignment_score': 57,
        'previous_cgpa': 5.9,
        'backlogs': 3,
        'study_hours': 2.8,
        'academic_performance': 60,
    }

    response = client.post('/predict', json=payload)
    assert response.status_code == 200
    body = response.json()
    assert 'risk_level' in body
    assert 'probability' in body


def test_invalid_input_is_rejected(client):
    bad_payload = {
        'student_id': 'X',
        'age': 10,
        'gender': 'Female',
        'course': 'B.Sc. Computer Science',
        'semester': 13,
        'attendance': 101,
        'previous_semester_marks': 75,
        'current_internal_marks': 70,
        'assignment_score': 80,
        'previous_cgpa': 7.5,
        'backlogs': -1,
        'study_hours': 1,
        'academic_performance': 80,
    }

    response = client.post('/predict', json=bad_payload)
    assert response.status_code == 422


def test_analytics_overview(client):
    response = client.get('/analytics/overview')
    assert response.status_code == 200
    body = response.json()
    assert 'medium_risk' in body
    assert body['total_students'] >= 0


def test_model_metrics_available(client):
    response = client.get('/model/metrics')
    # Model may be trained during startup; accept 200 or 404.
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        body = response.json()
        assert 'confusion_matrix' in body
        assert isinstance(body['confusion_matrix'], list)


def test_student_search_and_pagination(client):
    # Test pagination query params
    response = client.get('/students?skip=0&limit=5')
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) <= 5

    # Test search query param
    search_res = client.get('/students?search=TEST')
    assert search_res.status_code == 200
    assert isinstance(search_res.json(), list)


def test_analytics_trends(client):
    response = client.get('/analytics/trends')
    assert response.status_code == 200
    body = response.json()
    assert 'course_breakdown' in body
    assert 'attendance_by_risk' in body
    assert 'academic_by_risk' in body
    assert 'backlogs_by_risk' in body
    assert isinstance(body['course_breakdown'], list)



