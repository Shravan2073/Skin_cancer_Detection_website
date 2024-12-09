import pytest
from app import create_app, db
from app.models import User, Doctor, Patient

@pytest.fixture
def app():
    app = create_app('config.TestConfig')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def init_database(app):
    with app.app_context():
        # Create test users
        admin = User(username='admin', email='admin@test.com', role='admin')
        admin.set_password('password')
        doctor = User(username='doctor', email='doctor@test.com', role='doctor')
        doctor.set_password('password')
        patient = User(username='patient', email='patient@test.com', role='patient')
        patient.set_password('password')

        db.session.add_all([admin, doctor, patient])
        db.session.commit()

        # Create doctor and patient profiles
        doctor_profile = Doctor(user_id=doctor.id, specialization='Dermatology', qualifications='MD', university='Test University')
        patient_profile = Patient(user_id=patient.id, date_of_birth='1990-01-01', medical_history='None')

        db.session.add_all([doctor_profile, patient_profile])
        db.session.commit()

        yield

        db.session.remove()
        db.drop_all()

