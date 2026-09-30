import requests
from config import ADZUNA_APP_ID, ADZUNA_APP_KEY, DEFAULT_LOCATION, DEFAULT_RADIUS_KM

BASE_URL = "https://api.adzuna.com/v1/api/jobs/us/search"

def fetch_jobs(keywords="technical support", page=1):
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": 50,
        "what": keywords,
        "where": DEFAULT_LOCATION,
        "distance": DEFAULT_RADIUS_KM,
        "content-type": "application/json",
        "full_time": 1,
    }

    try:
        response = requests.get(f"{BASE_URL}/{page}", params=params)
        response.raise_for_status()
        data = response.json()
        return normalize(data.get("results", []))
    except requests.RequestException as e:
        print(f"Adzuna fetch error: {e}")
        return []

def normalize(listings):
    normalized = []
    for job in listings:
        normalized.append({
            "id": f"adzuna_{job['id']}",
            "title": job.get("title", ""),
            "company": job.get("company", {}).get("display_name", "Unknown"),
            "location": job.get("location", {}).get("display_name", ""),
            "salary_min": job.get("salary_min"),
            "salary_max": job.get("salary_max"),
            "description": job.get("description", ""),
            "url": job.get("redirect_url", ""),
            "source": "adzuna",
            "date_posted": job.get("created", ""),
            "remote": 1 if "remote" in job.get("title", "").lower()
                      or "remote" in job.get("description", "").lower()
                      else 0
        })
    return normalized
