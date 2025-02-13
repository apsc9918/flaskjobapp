from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

db = SQLAlchemy()

app = Flask(__name__)

# Use the correct key from your .env file
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.String(100), nullable=False)
    roles = db.Column(db.String(200), nullable=True)
    requirements = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"Job('{self.job_title}', '{self.location}', '{self.salary}')"
    
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    applicant_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    resume = db.Column(db.String(200), nullable=True)  # Could store a file path or URL
    cover_letter = db.Column(db.Text, nullable=True)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign key to the Job model
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    
    # Relationship: an Application is linked to a specific Job
    job = db.relationship('Job', backref=db.backref('applications', lazy=True))

    def __repr__(self):
        return f"Application('{self.applicant_name}', '{self.email}', job_id={self.job_id})"
