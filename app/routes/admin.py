from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import User, Doctor, Patient
from app import db

bp = Blueprint('admin', __name__, url_prefix='/admin')

# @bp.before_request
# @login_required
# def check_admin():
    # if not current_user.role == 'admin':
    #     flash('Access denied. Admin privileges required.')
    #     return redirect(url_for('main.index'))

@bp.route('/')
def dashboard():
    doctors = Doctor.query.all()
    patients = Patient.query.all()
    return render_template('admin/dashboard.html', doctors=doctors, patients=patients)

@bp.route('/create_doctor', methods=['GET', 'POST'])
def create_doctor():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        specialization = request.form['specialization']
        qualifications = request.form['qualifications']
        university = request.form['university']

        user = User(username=username, email=email, role='doctor')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        doctor = Doctor(user_id=user.id, specialization=specialization,
                        qualifications=qualifications, university=university)
        db.session.add(doctor)
        db.session.commit()

        flash('Doctor account created successfully.')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/create_doctor.html')

@bp.route('/view_profiles')
def view_profiles():
    doctors = Doctor.query.all()
    patients = Patient.query.all()
    return render_template('admin/view_profiles.html', doctors=doctors, patients=patients)

