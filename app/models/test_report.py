from app import db
from datetime import datetime

class TestReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    image_path = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    ml_prediction = db.Column(db.String(100))
    status = db.Column(db.String(20), default='Pending')

    patient = db.relationship('Patient', backref=db.backref('test_reports', lazy=True))
    doctor = db.relationship('Doctor', backref=db.backref('test_reports', lazy=True))

    def __repr__(self):
        return f'<TestReport {self.id}>'

