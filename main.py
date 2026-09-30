from database import initialize_db, insert_job
from connectors.adzuna import fetch_jobs as adzuna_fetch
from connectors.muse import fetch_jobs as muse_fetch
from config import SOURCES

def run_fetch(keywords="technical support", location=None):
    print("Initializing database...")
    initialize_db()

    total = 0

    if SOURCES.get("adzuna"):
        print(f"Fetching from Adzuna: '{keywords}'...")
        jobs = adzuna_fetch(keywords=keywords, location=location) if location else adzuna_fetch(keywords=keywords)
        for job in jobs:
            insert_job(job)
        total += len(jobs)
        print(f"Adzuna: {len(jobs)} listings fetched")

    if SOURCES.get("muse"):
        print(f"Fetching from The Muse: '{keywords}'...")
        jobs = muse_fetch(keywords=keywords)
        for job in jobs:
            insert_job(job)
        total += len(jobs)
        print(f"Muse: {len(jobs)} listings fetched")

    print(f"\nTotal fetched: {total} listings")

if __name__ == "__main__":
    import sys
    keywords = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "technical support"
    run_fetch(keywords=keywords)
