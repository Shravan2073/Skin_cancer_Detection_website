import pytest
from flask_login import login_user
from app.models import User, TestReport
from io import BytesIO

def test_patient_dashboard(client, init_database):
    patient = User.query.filter_by(username='patient').first()
    with client.session_transaction() as sess:
        sess['user_id'] = patient.id
    login_user(patient)
    
    response = client.get('/patient/')
    assert response.status_code == 200
    assert b'Patient Dashboard' in response.data

def test_submit_test(client, init_database):
    patient = User.query.filter_by(username='patient').first()
    with client.session_transaction() as sess:
        sess['user_id'] = patient.id
    login_user(patient)
    
    data = {
        'description': 'Test description',
        'image': (BytesIO(b'my file contents'), 'test.jpg')
    }
    response = client.post('/patient/submit_test', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert response.status_code == 200
    assert b'Test report submitted successfully' in response.data
    
    test_report = TestReport.query.filter_by(patient_id=patient.id).first()
    assert test_report is not None
    assert test_report.description == 'Test description'

