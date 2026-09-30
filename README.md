# Job Search Tool

A small, locally run job aggregator. It pulls listings from public job APIs
(Adzuna, The Muse), stores them in a local SQLite database, and serves a simple
web page where you can filter by keyword, minimum salary, and remote-only.

No third-party Python packages are required beyond whatever the connectors use
for HTTP requests.

## Features

- Fetch listings from multiple sources (toggle each in `config.py`)
- De-duplicated storage in SQLite (`INSERT OR IGNORE` on listing ID)
- Filter by keyword (title/description), minimum salary, and remote-only
- Runs entirely on localhost

## Project layout

```
.
├── main.py          # CLI: fetch listings into the database
├── server.py        # Local web server + JSON API (port 8765)
├── database.py      # SQLite schema, insert, and query helpers
├── config.py        # Settings loader (reads credentials.json)
├── credentials.example.json  # Template; copy to credentials.json (git-ignored)
├── connectors/
│   ├── adzuna.py    # Adzuna API connector
│   └── muse.py      # The Muse API connector
└── frontend/
    ├── index.html
    └── app.js
```

Each connector exposes `fetch_jobs(keywords=...)` and returns a list of dicts
with the fields the `jobs` table expects: `id`, `title`, `company`, `location`,
`description`, `url`, `source`, and optionally `salary_min`, `salary_max`,
`date_posted`, `remote`.

## Setup

1. Get free API credentials from [Adzuna](https://developer.adzuna.com/).
2. Copy the example credentials file and fill it in:

   ```bash
   cp credentials.example.json credentials.json
   ```

   ```json
   {
     "adzuna_app_id": "your_app_id",
     "adzuna_app_key": "your_app_key",
     "location": "Your City, State",
     "radius_km": 40,
     "min_salary": 41600
   }
   ```

   `credentials.json` is git-ignored. Never commit it.
3. Run everything from the project root (paths like `frontend/index.html` and
   `job_search.db` are relative to the working directory).

## Usage

**Fetch listings from the command line:**

```bash
python main.py                      # defaults to "technical support"
python main.py help desk analyst    # any keywords
```

**Start the web UI:**

```bash
python server.py
# open http://localhost:8765
```

Use the **Fetch** button in the UI to pull new listings, then filter the
results with the keyword, salary, and remote controls.

## API

| Endpoint | Description |
|---|---|
| `GET /api/jobs?min_salary=&remote_only=&keyword=` | Query stored listings |
| `GET /api/fetch?keyword=` | Fetch fresh listings from all sources and store them |

## Configuration

Settings are read from `credentials.json`. Environment variables override the file.

| Setting | `credentials.json` key | Env var | Default |
|---|---|---|---|
| Adzuna app ID | `adzuna_app_id` | `ADZUNA_APP_ID` | *(none)* |
| Adzuna app key | `adzuna_app_key` | `ADZUNA_APP_KEY` | *(none)* |
| Search location | `location` | `JOB_LOCATION` | `Austin, Texas` |
| Search radius (km) | `radius_km` | `JOB_RADIUS_KM` | `40` |
| Minimum salary | `min_salary` | `JOB_MIN_SALARY` | `41600` |

Enable or disable sources in the `SOURCES` dict in `config.py`.

## Notes

- The salary filter only matches listings that report a minimum salary;
  listings with no salary data are hidden while a minimum is set. Set the
  minimum to `0` to see everything.
- The database (`job_search.db`) is created on first run and is git-ignored.
- The server binds to `localhost` only and is not intended to be exposed publicly.
