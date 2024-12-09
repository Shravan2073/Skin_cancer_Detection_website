from app import db
from .user import User

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('doctor', uselist=False))
    specialization = db.Column(db.String(100))
    qualifications = db.Column(db.Text)
    university = db.Column(db.String(200))

    def __repr__(self):
        return f'<Doctor {self.user.username}>'

