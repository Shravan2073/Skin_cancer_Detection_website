import pytest
from flask_login import login_user
from app.models import User, Doctor

def test_admin_dashboard(client, init_database):
    admin = User.query.filter_by(username='admin').first()
    with client.session_transaction() as sess:
        sess['user_id'] = admin.id
    login_user(admin)
    
    response = client.get('/admin/')
    assert response.status_code == 200
    assert b'Admin Dashboard' in response.data

def test_create_doctor(client, init_database):
    admin = User.query.filter_by(username='admin').first()
    with client.session_transaction() as sess:
        sess['user_id'] = admin.id
    login_user(admin)
    
    response = client.post('/admin/create_doctor', data={
        'username': 'newdoctor',
        'email': 'newdoctor@test.com',
        'password': 'password',
        'specialization': 'Oncology',
        'qualifications': 'MD, PhD',
        'university': 'Test Medical School'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Doctor account created successfully' in response.data
    
    new_doctor = Doctor.query.filter_by(user__username='newdoctor').first()
    assert new_doctor is not None
    assert new_doctor.specialization == 'Oncology'

