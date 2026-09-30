import sqlite3
from datetime import datetime

DB_PATH = "job_search.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            title TEXT,
            company TEXT,
            location TEXT,
            salary_min REAL,
            salary_max REAL,
            description TEXT,
            url TEXT,
            source TEXT,
            date_posted TEXT,
            date_fetched TEXT,
            remote INTEGER DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()

def insert_job(job):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT OR IGNORE INTO jobs
        (id, title, company, location, salary_min, salary_max,
         description, url, source, date_posted, date_fetched, remote)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        job['id'],
        job['title'],
        job['company'],
        job['location'],
        job.get('salary_min'),
        job.get('salary_max'),
        job['description'],
        job['url'],
        job['source'],
        job.get('date_posted'),
        datetime.now().isoformat(),
        job.get('remote', 0)
    ))

    conn.commit()
    conn.close()

def fetch_jobs(min_salary=None, remote_only=False, keyword=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM jobs WHERE 1=1"
    params = []

    if min_salary:
        query += " AND salary_min >= ?"
        params.append(min_salary)

    if remote_only:
        query += " AND remote = 1"

    if keyword:
        query += " AND (title LIKE ? OR description LIKE ?)"
        params.extend([f"%{keyword}%", f"%{keyword}%"])

    query += " ORDER BY date_posted DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows
