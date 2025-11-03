from flask import Flask, jsonify, render_template
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

def get_db_connection():
    """Create and return a database connection using DATABASE_URL environment variable."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    return psycopg2.connect(database_url, cursor_factory=RealDictCursor)


@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')


@app.route('/jobs')
def jobs():
    """Render the jobs listing page."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM job_postings ORDER BY id")
        jobs = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('jobs.html', jobs=jobs, count=len(jobs))
    except Exception as e:
        return render_template('jobs.html', jobs=[], count=0, error=str(e))


@app.route('/jobs/<job_id>')
def job_detail(job_id):
    """Render a single job details page."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM job_postings WHERE id = %s", (job_id,))
        job = cursor.fetchone()
        cursor.close()
        conn.close()

        if job is None:
            return render_template('job_detail.html', job=None, error="Job not found"), 404

        return render_template('job_detail.html', job=job)
    except Exception as e:
        return render_template('job_detail.html', job=None, error=str(e)), 500


@app.route('/api/jobs')
def api_jobs():
    """API endpoint: Fetch all job postings from the database as JSON."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM job_postings ORDER BY id")
        jobs = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"jobs": jobs, "count": len(jobs)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
