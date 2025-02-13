# job_queries.py
from models import app, Job  # Import from models.py

def get_jobs_in_bangalore():
    # You don't need to push an app context if this function is only called within a request.
    # However, if you intend to use it outside a request (e.g., in a standalone script), use app.app_context():
    with app.app_context():
        jobs_in_bangalore = Job.query.all()
        job_dicts = []
        for job in jobs_in_bangalore:
            job_data = {
                "id": job.id,
                "job_title": job.job_title,
                "location": job.location,
                "salary": job.salary,
                "roles": job.roles,
                "requirements": job.requirements
            }
            job_dicts.append(job_data)
        return job_dicts
    
def get_job_by_id(job_id):
    with app.app_context():
        job = Job.query.get(job_id)
        if job:
            job_data = {
                "id": job.id,
                "job_title": job.job_title,
                "location": job.location,
                "salary": job.salary,
                "roles": job.roles,
                "requirements": job.requirements
            }
            return job_data
        else:
            return None

if __name__ == '__main__':
    # For standalone testing:
    jobs = get_jobs_in_bangalore()
    print(jobs)
