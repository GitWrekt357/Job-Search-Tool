"""Configuration.

Secrets and personal settings live in credentials.json (gitignored), next to this
file. Copy credentials.example.json to credentials.json and fill it in.
Environment variables, if set, override the file.
"""
import json
import os
import sys

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_CREDENTIALS_PATH = os.path.join(_BASE_DIR, "credentials.json")


def _load_credentials():
    try:
        with open(_CREDENTIALS_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(
            "Warning: credentials.json not found. Copy credentials.example.json "
            "to credentials.json and add your Adzuna keys.",
            file=sys.stderr,
        )
    except json.JSONDecodeError as e:
        print(f"Warning: credentials.json is not valid JSON: {e}", file=sys.stderr)
    return {}


_creds = _load_credentials()


def _get(name, env_var, default=""):
    return os.environ.get(env_var) or _creds.get(name, default)


# API keys (free at https://developer.adzuna.com/)
ADZUNA_APP_ID = _get("adzuna_app_id", "ADZUNA_APP_ID")
ADZUNA_APP_KEY = _get("adzuna_app_key", "ADZUNA_APP_KEY")

# Search defaults
DEFAULT_LOCATION = _get("location", "JOB_LOCATION", "Austin, Texas")
DEFAULT_RADIUS_KM = int(_get("radius_km", "JOB_RADIUS_KM", 40))  # ~25 miles
DEFAULT_MIN_SALARY = int(_get("min_salary", "JOB_MIN_SALARY", 41600))  # $20/hr annualized

# Job sources toggle - easy to add new ones later
SOURCES = {
    "adzuna": True,
    "muse": True,
}
