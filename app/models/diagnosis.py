from app import db
from datetime import datetime

class Diagnosis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_report_id = db.Column(db.Integer, db.ForeignKey('test_report.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    severity = db.Column(db.String(20))
    cancer_type = db.Column(db.String(100))
    other_condition = db.Column(db.String(100))
    medication = db.Column(db.Text)
    frequency = db.Column(db.String(50))
    directions = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    test_report = db.relationship('TestReport', backref=db.backref('diagnosis', uselist=False))
    doctor = db.relationship('Doctor', backref=db.backref('diagnoses', lazy=True))

    def __repr__(self):
        return f'<Diagnosis {self.id}>'

