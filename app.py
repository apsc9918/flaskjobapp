# app.py
from flask import render_template, request, redirect, url_for
from models import app  # Import the Flask app and models from models.py
from job_queries import get_jobs_in_bangalore, get_job_by_id
from models import db, Application
import os
from werkzeug.utils import secure_filename

# Add these configurations to your app
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    # If this function is executed during a request, an application context is already pushed.
    job_openings = get_jobs_in_bangalore()
    return render_template('home.html', job_openings=job_openings)

# @app.route('/application/<id>')
# def application():
#     # If this function is executed during a request, an application context is already pushed.
#     return render_template('application.html')

@app.route('/application/<id>')
def show_application(id):
    open_job = get_job_by_id(id)
    return render_template('application.html', job=open_job)

@app.route('/application/<id>/submit_application', methods=['POST'])
def apply_for_job(id):
    if request.method == 'POST':
        # Get form data
        applicant_name = request.form.get('applicant_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        cover_letter = request.form.get('cover_letter')
        
        # Handle resume file upload
        resume_path = None
        if 'resume' in request.files:
            file = request.files['resume']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                resume_path = file_path

        # Create new application
        new_application = Application(
            applicant_name=applicant_name,
            email=email,
            phone=phone,
            resume=resume_path,
            cover_letter=cover_letter,
            job_id=id
        )

        try:
            db.session.add(new_application)
            db.session.commit()
            
            # Get the job details for the success page
            job = get_job_by_id(id)
            
            return render_template('success.html', 
                                 application=new_application,
                                 job=job)
        except Exception as e:
            db.session.rollback()
            # In a production environment, you'd want to log this error
            return "An error occurred while submitting your application.", 500

    return redirect(url_for('show_application', id=id))


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port=8080, debug=True)
