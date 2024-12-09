from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Doctor, TestReport, Appointment, Diagnosis, Treatment
from app import db

bp = Blueprint('doctor', __name__, url_prefix='/doctor')

@bp.before_request
@login_required
def check_doctor():
    if not current_user.role == 'doctor':
        flash('Access denied. Doctor privileges required.')
        return redirect(url_for('main.index'))

@bp.route('/')
def dashboard():
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    pending_reports = TestReport.query.filter_by(status='Pending').all()
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
    return render_template('doctor/dashboard.html', doctor=doctor, pending_reports=pending_reports, appointments=appointments)

@bp.route('/profile')
def profile():
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    return render_template('doctor/profile.html', doctor=doctor)

@bp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    if request.method == 'POST':
        doctor.specialization = request.form['specialization']
        doctor.qualifications = request.form['qualifications']
        doctor.university = request.form['university']
        db.session.commit()
        flash('Profile updated successfully.')
        return redirect(url_for('doctor.profile'))
    return render_template('doctor/edit_profile.html', doctor=doctor)

@bp.route('/queries')
def queries():
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    test_reports = TestReport.query.filter_by(status='Pending').all()
    return render_template('doctor/queries.html', doctor=doctor, test_reports=test_reports)

@bp.route('/respond_query/<int:report_id>', methods=['GET', 'POST'])
def respond_query(report_id):
    report = TestReport.query.get_or_404(report_id)
    if request.method == 'POST':
        severity = request.form['severity']
        cancer_type = request.form['cancer_type']
        other_condition = request.form['other_condition']
        medication = request.form['medication']
        frequency = request.form['frequency']
        directions = request.form['directions']

        diagnosis = Diagnosis(test_report_id=report.id, doctor_id=current_user.doctor.id,
                              severity=severity, cancer_type=cancer_type,
                              other_condition=other_condition, medication=medication,
                              frequency=frequency, directions=directions)
        db.session.add(diagnosis)

        report.status = 'Responded'
        report.doctor_id = current_user.doctor.id
        db.session.commit()

        flash('Response submitted successfully.')
        return redirect(url_for('doctor.queries'))
    return render_template('doctor/respond_query.html', report=report)

