from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from database import fetch_jobs, initialize_db
initialize_db()
from database import fetch_jobs
from config import DEFAULT_MIN_SALARY

class JobHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.serve_file("frontend/index.html", "text/html")
        elif self.path == "/app.js":
            self.serve_file("frontend/app.js", "application/javascript")
        elif self.path.startswith("/api/jobs"):
            self.serve_jobs()
        elif self.path.startswith("/api/fetch"):
            self.serve_fetch()
        else:
            self.send_response(404)
            self.end_headers()

    def serve_file(self, path, content_type):
        try:
            with open(path, "r") as f:
                content = f.read().encode()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()

    def serve_jobs(self):
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        min_salary = float(params.get("min_salary", [DEFAULT_MIN_SALARY])[0])
        remote_only = params.get("remote_only", ["false"])[0] == "true"
        keyword = params.get("keyword", [None])[0]

        jobs = fetch_jobs(
            min_salary=min_salary,
            remote_only=remote_only,
            keyword=keyword
        )

        job_list = []
        for job in jobs:
            job_list.append({
                "id": job[0],
                "title": job[1],
                "company": job[2],
                "location": job[3],
                "salary_min": job[4],
                "salary_max": job[5],
                "description": job[6][:300] + "..." if job[6] and len(job[6]) > 300 else job[6],
                "url": job[7],
                "source": job[8],
                "date_posted": job[9],
                "remote": bool(job[11])
            })

        response = json.dumps(job_list).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(response)

    def serve_fetch(self):
        from urllib.parse import urlparse, parse_qs
        from connectors.adzuna import fetch_jobs as adzuna_fetch
        from database import insert_job
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        keyword = params.get("keyword", ["technical support"])[0]
        jobs = adzuna_fetch(keywords=keyword)
        for job in jobs:
            insert_job(job)
        from connectors.muse import fetch_jobs as muse_fetch
        jobs = adzuna_fetch(keywords=keyword)
        for job in jobs:
            insert_job(job)
        muse_jobs = muse_fetch(keywords=keyword)
        for job in muse_jobs:
            insert_job(job)
        response = json.dumps({"message": f"Fetched {len(jobs)} listings"}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(response)

    def log_message(self, format, *args):
        pass

def start_server(port=8765):
    server = HTTPServer(("localhost", port), JobHandler)
    print(f"Job search running at http://localhost:{port}")
    server.serve_forever()

if __name__ == "__main__":
    start_server()
