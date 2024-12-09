from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app.models import Patient, TestReport, Appointment
from app import db
from app.utils import predict_cancer_type, allowed_file, save_uploaded_file, validate_image
from werkzeug.utils import secure_filename
import os
from datetime import datetime

bp = Blueprint('patient', __name__, url_prefix='/patient')

@bp.before_request
@login_required
def check_patient():
    if not current_user.role == 'patient':
        flash('Access denied. Patient privileges required.', 'error')
        return redirect(url_for('main.index'))

@bp.route('/')
def dashboard():
    print(Patient.query.all())
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    test_reports = TestReport.query.filter_by(patient_id=patient.id).order_by(TestReport.submission_date.desc()).all()
    appointments = Appointment.query.filter_by(patient_id=patient.id).order_by(Appointment.date_time).all()
    return render_template('patient/dashboard.html', patient=patient, test_reports=test_reports, appointments=appointments)

@bp.route('/profile')
def profile():
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    return render_template('patient/profile.html', patient=patient)

@bp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    if request.method == 'POST':
        try:
            patient.date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date()
            patient.medical_history = request.form['medical_history']
            db.session.commit()
            flash('Profile updated successfully.', 'success')
            return redirect(url_for('patient.profile'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while updating your profile: {str(e)}', 'error')
    return render_template('patient/edit_profile.html', patient=patient)

@bp.route('/submit_test', methods=['GET', 'POST'])
def submit_test():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        
        image = request.files['image']
        description = request.form['description']
        
        if image.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path_rel = os.path.join('uploads', filename)
            print(image_path_rel)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_path_rel)
            image.save(image_path)
            
            if not validate_image(image_path):
                os.remove(image_path)
                flash('Invalid image file', 'error')
                return redirect(request.url)
            
            try:
                ml_prediction = predict_cancer_type(image_path)
                
                test_report = TestReport(
                    patient_id=current_user.patient.id,
                    image_path=image_path_rel,
                    description=description,
                    ml_prediction=ml_prediction
                )
                db.session.add(test_report)
                db.session.commit()
                
                flash('Test report submitted successfully.', 'success')
                return redirect(url_for('patient.dashboard'))
            except Exception as e:
                db.session.rollback()
                os.remove(image_path)
                flash(f'An error occurred while submitting your test: {str(e)}', 'error')
                return redirect(request.url)
        else:
            flash('Allowed image types are png, jpg, jpeg, gif', 'error')
    
    return render_template('patient/submit_test.html')

@bp.route('/view_result/<int:report_id>')
def view_result(report_id):
    report = TestReport.query.get_or_404(report_id)
    if report.patient_id != current_user.patient.id:
        flash('Access denied.', 'error')
        return redirect(url_for('patient.dashboard'))
    return render_template('patient/view_result.html', report=report)

@bp.route('/appointments')
def appointments():
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    appointments = Appointment.query.filter_by(patient_id=patient.id).order_by(Appointment.date_time).all()
    return render_template('patient/appointments.html', appointments=appointments)

@bp.route('/request_appointment_change/<int:appointment_id>', methods=['POST'])
def request_appointment_change(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    if appointment.patient_id != current_user.patient.id:
        flash('Access denied.', 'error')
        return redirect(url_for('patient.appointments'))
    
    try:
        new_date = datetime.strptime(request.form['new_date'], '%Y-%m-%dT%H:%M')
        appointment.status = 'Change Requested'
        appointment.notes = f"Patient requested change to: {new_date.strftime('%Y-%m-%d %H:%M')}"
        db.session.commit()
        flash('Appointment change request submitted.', 'success')
    except ValueError:
        flash('Invalid date format. Please use the date picker.', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred while requesting the appointment change: {str(e)}', 'error')
    
    return redirect(url_for('patient.appointments'))

@bp.route('/cancel_appointment/<int:appointment_id>', methods=['POST'])
def cancel_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    if appointment.patient_id != current_user.patient.id:
        flash('Access denied.', 'error')
        return redirect(url_for('patient.appointments'))
    
    try:
        appointment.status = 'Cancelled'
        db.session.commit()
        flash('Appointment cancelled successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred while cancelling the appointment: {str(e)}', 'error')
    
    return redirect(url_for('patient.appointments'))

