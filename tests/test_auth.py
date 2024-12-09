import pytest
from flask_login import current_user
from app.models import User

def test_login(client, init_database):
    response = client.post('/login', data={
        'username': 'patient',
        'password': 'password'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome' in response.data
    assert current_user.is_authenticated

def test_logout(client, init_database):
    client.post('/login', data={
        'username': 'patient',
        'password': 'password'
    })
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data
    assert not current_user.is_authenticated

def test_register(client):
    response = client.post('/register', data={
        'username': 'newuser',
        'email': 'newuser@test.com',
        'password': 'password'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Registration successful' in response.data
    user = User.query.filter_by(username='newuser').first()
    assert user is not None

