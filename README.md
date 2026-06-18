# Job Connect

A bilingual (English/Tamil) job portal built with Streamlit, connecting blue-collar job seekers with job creators. Includes TF-IDF based smart matching, in-app chat, an admin dashboard, and a government welfare schemes lookup.

## Features

- Job seeker and job creator registration/login (mock OTP flow)
- Skill-based job matching using TF-IDF + cosine similarity
- Real-time-ish chat between job creators and seekers (auto-refreshing)
- Admin dashboard with user/job filtering
- Government scheme browser and admin-editable scheme list
- English and Tamil language toggle

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app will create `job_portal.db` (SQLite) automatically on first run, along with a default admin account:

```
Mobile: 9999999999
Password: admin123
```

`government_schemes.xlsx` is included with a starter list of Indian government welfare schemes. If missing, the app regenerates a default version automatically.

## Bulk-importing job seekers

`import_script.py` can bulk-load job seekers from an Excel file (default: `job_seeker_details.xlsx`) into the database, auto-detecting name/mobile/location/skill columns and skipping duplicates/invalid numbers.

```bash
python import_script.py
```

A small sample file with fake data is included so you can try this out safely. **All bulk-imported users get the placeholder password `123`** — this is meant for demos only.

## ⚠️ Known limitations (this is a demo/learning project, not production-ready)

- Passwords are stored and compared in **plaintext**. Don't reuse a real password if you register an account here.
- OTP verification is hardcoded to `123456` — there's no real SMS integration.
- No rate limiting, CSRF protection, or session expiry.
- `job_portal.db` is excluded from version control via `.gitignore` — never commit a database containing real user data.

## Tech stack

Streamlit, SQLite, pandas, scikit-learn (TF-IDF/cosine similarity for matching), openpyxl.
