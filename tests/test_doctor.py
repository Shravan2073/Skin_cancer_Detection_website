import pytest
from flask_login import login_user
from app.models import User, TestReport, Diagnosis

def test_doctor_dashboard(client, init_database):
    doctor = User.query.filter_by(username='doctor').first()
    with client.session_transaction() as sess:
        sess['user_id'] = doctor.id
    login_user(doctor)
    
    response = client.get('/doctor/')
    assert response.status_code == 200
    assert b'Doctor Dashboard' in response.data

def test_respond_to_query(client, init_database):
    doctor = User.query.filter_by(username='doctor').first()
    with client.session_transaction() as sess:
        sess['user_id'] = doctor.id
    login_user(doctor)
    
    # Create a test report
    patient = User.query.filter_by(username='patient').first()
    test_report = TestReport(patient_id=patient.id, image_path='test.jpg', description='Test description', ml_prediction='Test prediction')
    db.session.add(test_report)
    db.session.commit()
    
    response = client.post(f'/doctor/respond_query/{test_report.id}', data={
        'severity': 'moderate',
        'cancer_type': 'Melanoma',
        'medication': 'Test medication',
        # ...existing code...
    })
    assert response.status_code == 200
    assert b'Response submitted successfully' in response.data
    
    diagnosis = Diagnosis.query.filter_by(test_report_id=test_report.id).first()
    assert diagnosis is not None
    assert diagnosis.severity == 'moderate'
    assert diagnosis.cancer_type == 'Melanoma'

