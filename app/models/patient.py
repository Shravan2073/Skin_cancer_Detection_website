from app import db
from .user import User

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('patient', uselist=False))
    date_of_birth = db.Column(db.Date)
    medical_history = db.Column(db.Text)

    def __repr__(self):
        return f'<Patient {self.user.username}>'

