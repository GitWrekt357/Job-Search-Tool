import requests

BASE_URL = "https://www.themuse.com/api/public/jobs"

def fetch_jobs(keywords="technical support", page=0):
    params = {
        "descending": "true",
        "page": page,
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return normalize(data.get("results", []), keywords)
    except requests.RequestException as e:
        print(f"Muse fetch error: {e}")
        return []

def normalize(listings, keywords):
    normalized = []
    keywords_lower = keywords.lower().split()

    for job in listings:
        title = job.get("name", "").lower()
        contents = job.get("contents", "").lower()

        # filter by keyword since Muse API doesn't support keyword search directly
        if not any(kw in title or kw in contents for kw in keywords_lower):
            continue

        locations = job.get("locations", [])
        location_str = locations[0].get("name", "") if locations else "Remote"

        normalized.append({
            "id": f"muse_{job['id']}",
            "title": job.get("name", ""),
            "company": job.get("company", {}).get("name", "Unknown"),
            "location": location_str,
            "salary_min": None,
            "salary_max": None,
            "description": job.get("contents", ""),
            "url": job.get("refs", {}).get("landing_page", ""),
            "source": "muse",
            "date_posted": job.get("publication_date", ""),
            "remote": 1 if "flexible" in location_str.lower()
                      or "remote" in location_str.lower()
                      else 0
        })
    return normalized
