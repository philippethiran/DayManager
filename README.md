# DayManager

Local single-user daily task manager (manual tasks MVP).

## Prerequisites

- Python 3.9+
- Node.js 18+ and npm

## Backend (FastAPI + SQLite)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs  
Health: http://localhost:8000/api/health

Run tests:

```bash
cd backend
source .venv/bin/activate
python -m pytest
```

## Frontend (Angular)

In a second terminal:

```bash
cd frontend
npm start
```

Open http://localhost:4200 — the UI calls the API at http://localhost:8000.

## MVP scope

- View and add manual tasks for a calendar day (local browser timezone)
- Optional time and done checkbox per task
- Google Calendar integration is deferred (see `_bmad-output/implementation-artifacts/deferred-work.md`)
