# Job Connect

A bilingual (English/Tamil) job portal built with Streamlit, connecting blue-collar job seekers with job creators. Includes TF-IDF based smart matching, in-app chat, an admin dashboard, and a government welfare schemes lookup.

## Features

- Job seeker and job creator registration/login (mock OTP flow)
- Skill-based job matching using TF-IDF + cosine similarity
- Auto-refreshing chat between job creators and seekers
- Admin dashboard with user/job filtering
- Government scheme browser and admin-editable scheme list
- English and Tamil language toggle
- Passwords stored as salted PBKDF2-SHA256 hashes

## Setup

```bash
pip install -r requirements.txt
```

Set an admin password, then start the app:

```bash
# Windows (PowerShell)
$env:ADMIN_PASSWORD="choose-a-strong-password"

# Mac / Linux
export ADMIN_PASSWORD="choose-a-strong-password"

streamlit run app.py
```

On first run the app creates `job_portal.db` (SQLite) and an admin account with mobile `9999999999` and the password from `ADMIN_PASSWORD`. If the variable is not set, a random temporary password is printed once in the terminal.

`government_schemes.xlsx` is included with a starter list of Indian government welfare schemes. If missing, the app regenerates a default version automatically.

## Bulk-importing job seekers

`import_script.py` can bulk-load job seekers from an Excel file (default: `job_seeker_details.xlsx`) into the database, auto-detecting name/mobile/location/skill columns and skipping duplicates/invalid numbers.

```bash
python import_script.py
```

A small sample file with fake data is included so you can try this out safely. Bulk-imported users get the placeholder password `123` (stored hashed). This is meant for demos only.

## ⚠️ Known limitations (this is a demo/learning project, not production-ready)

- OTP verification is hardcoded to `123456`. There is no real SMS integration.
- The Aadhaar number is stored unencrypted. Do not enter real Aadhaar numbers.
- No rate limiting, CSRF protection, or session expiry.
- `job_portal.db` is excluded from version control via `.gitignore`. Never commit a database containing real user data.

## Tech stack

Streamlit, SQLite, pandas, scikit-learn (TF-IDF/cosine similarity for matching), openpyxl. Password hashing is in `security.py` (Python standard library, PBKDF2-SHA256).
