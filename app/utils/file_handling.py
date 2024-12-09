import os
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """
    Check if the file has an allowed extension.
    
    :param filename: Name of the file
    :return: Boolean indicating if the file extension is allowed
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file):
    """
    Save the uploaded file to the upload folder.
    
    :param file: File object from request.files
    :return: Path where the file was saved
    """
    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    return file_path

def get_file_extension(filename):
    """
    Get the extension of a file.
    
    :param filename: Name of the file
    :return: File extension
    """
    return os.path.splitext(filename)[1]

def create_unique_filename(original_filename):
    """
    Create a unique filename to avoid overwriting existing files.
    
    :param original_filename: Original name of the file
    :return: Unique filename
    """
    base_name, extension = os.path.splitext(original_filename)
    return f"{base_name}_{os.urandom(8).hex()}{extension}"

def delete_file(file_path):
    """
    Delete a file from the server.
    
    :param file_path: Path to the file
    :return: Boolean indicating if the file was successfully deleted
    """
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False

