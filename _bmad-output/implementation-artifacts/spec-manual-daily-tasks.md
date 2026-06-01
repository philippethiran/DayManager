---
title: 'Manual daily tasks (MVP)'
type: 'feature'
created: '2026-06-01'
status: 'done'
baseline_commit: '967e69d685d43bf242f869cbe925d4c0276f38ce'
context:
  - '{project-root}/_bmad-output/project-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** DayManager has no runnable app yet. The user needs a local web UI to see and manage today’s manual tasks before Google Calendar integration.

**Approach:** Scaffold FastAPI + SQLite backend and Angular frontend. Persist manual tasks locally. Expose REST CRUD filtered by calendar date. The UI shows one day at a time (default: today in the browser’s local timezone) with list, add, toggle-done, and delete.

## Boundaries & Constraints

**Always:**
- Single-user, no authentication.
- Manual tasks only; no Google Calendar API calls in this pass.
- Follow `project-context.md`: services for business logic, Pydantic schemas at API boundary, Angular services for HTTP, `/api/` prefix, `snake_case` JSON from backend.
- Task fields: **title** (required), **optional time** (same calendar day), **done** boolean.
- “Day” is selected by the client as `YYYY-MM-DD` in the user’s local calendar; backend stores and filters by that date value (no server-side timezone conversion).
- Backend pytest coverage for API routes and core behaviors (minimum viable).
- Do not commit `.env`, secrets, or `*.db` files.

**Ask First:**
- Adding npm/Python dependencies beyond FastAPI, SQLAlchemy, Uvicorn, pytest stack, and a standard Angular CLI scaffold.
- Changing API field names or breaking the date-filter contract.

**Never:**
- User accounts, login, or multi-tenant data.
- Google Calendar sync (deferred — see `deferred-work.md`).
- Deploying to cloud or Docker packaging (local dev only).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| List day tasks | `GET /api/tasks?date=2026-06-01` | `200` JSON array of tasks for that date, sorted: timed tasks by time ascending, then untimed by title | `422` if date invalid |
| Create task | `POST /api/tasks` body `{ "title": "Buy milk", "task_date": "2026-06-01", "due_time": "09:30:00" }` | `201` created task with `id`, `is_done: false` | `422` if title empty or date invalid |
| Create untimed | `POST` with `due_time: null` | `201`, task appears after timed tasks in list | same as above |
| Toggle done | `PATCH /api/tasks/{id}` `{ "is_done": true }` | `200` updated task | `404` if missing id |
| Delete task | `DELETE /api/tasks/{id}` | `204` no body | `404` if missing id |
| Empty day | Valid date, no rows | `200` `[]` | N/A |
| Cross-day isolation | Tasks on `2026-06-01` and `2026-06-02` | List for each date returns only that day’s tasks | N/A |

</frozen-after-approval>

## Code Map

- `backend/` — new FastAPI application root (greenfield)
- `backend/app/main.py` — app factory, CORS for `http://localhost:4200`
- `backend/app/database.py` — SQLAlchemy engine, session dependency, SQLite file path
- `backend/app/models/task.py` — `Task` ORM model
- `backend/app/schemas/task.py` — Pydantic request/response models
- `backend/app/services/task_service.py` — CRUD + list-by-date sorting
- `backend/app/routes/tasks.py` — `/api/tasks` router
- `backend/tests/` — pytest using temp/in-memory SQLite
- `frontend/` — new Angular app (greenfield)
- `frontend/src/app/services/task.service.ts` — HTTP client for tasks API
- `frontend/src/app/components/day-view/` — day list, add form, done toggle, delete
- `frontend/src/app/app.config.ts` — provide HttpClient, API base URL for dev
- `.gitignore` — ignore `*.db`, `node_modules/`, `__pycache__/`, `.env`

## Tasks & Acceptance

**Execution:**
- [x] `.gitignore` — extend root ignore rules for DB, Python, Angular artifacts — keep repo clean
- [x] `backend/requirements.txt` — pin FastAPI, Uvicorn, SQLAlchemy, pytest, httpx — runnable local API
- [x] `backend/app/database.py` — SQLite session setup and `create_all` on startup for dev
- [x] `backend/app/models/task.py` — `Task` with `id`, `title`, `task_date`, `due_time` (nullable), `is_done`, `created_at`
- [x] `backend/app/schemas/task.py` — create/update/read schemas with validation (non-empty title)
- [x] `backend/app/services/task_service.py` — list-by-date sort, create, patch, delete
- [x] `backend/app/routes/tasks.py` — wire routes per I/O matrix
- [x] `backend/app/main.py` — mount router, CORS, startup DB init
- [x] `backend/tests/test_tasks_api.py` — cover matrix scenarios with TestClient
- [x] `frontend/` — Angular scaffold (CLI or minimal equivalent) with dev server on port 4200
- [x] `frontend/src/app/services/task.service.ts` — map API `snake_case` to frontend models
- [x] `frontend/src/app/components/day-view/` — date display (local today default), task list, add form, toggle, delete with loading/error states
- [x] `README.md` — how to run backend and frontend locally

**Acceptance Criteria:**
- Given backend and frontend running locally, when the user opens the app, then today’s date is shown and tasks for that date load (or empty list).
- Given the day view, when the user adds a task with title only, then it appears in the list marked not done.
- Given a task with an optional time, when listed with other tasks, then timed tasks sort before untimed tasks by time.
- Given an existing task, when the user toggles done, then the state persists after refresh.
- Given an existing task, when the user deletes it, then it disappears and does not return on refresh.
- Given `pytest` in `backend/`, when tests run, then all task API tests pass.

## Verification

**Commands:**
- `cd backend && python -m pytest` — expected: all tests pass
- `cd backend && uvicorn app.main:app --reload --port 8000` — expected: OpenAPI at `/docs`, health OK
- `cd frontend && npm start` — expected: app on `http://localhost:4200`, loads day view without console errors against running API

**Manual checks (if no CLI):**
- Add two tasks (one timed, one not) on the same day; confirm sort order in UI matches API.

## Spec Change Log

- **2026-06-01** — Initial implementation complete; review found no intent_gap or bad_spec. Patch: reload task list after create so sort matches API.

## Suggested Review Order

**API entry and wiring**

- FastAPI app, CORS, and DB init on startup.
  [`main.py:12`](../../backend/app/main.py#L12)

- REST routes delegating to the task service.
  [`tasks.py:14`](../../backend/app/routes/tasks.py#L14)

**Domain logic**

- List-by-date sort: timed first, then untimed by title.
  [`task_service.py:10`](../../backend/app/services/task_service.py#L10)

- ORM model and Pydantic schemas at the API boundary.
  [`task.py:11`](../../backend/app/models/task.py#L11)
  [`task.py:8`](../../backend/app/schemas/task.py#L8)

**Day view UI**

- Local date selection, load/create/toggle/delete with error states.
  [`day-view.component.ts:26`](../../frontend/src/app/components/day-view/day-view.component.ts#L26)

- HTTP client for `/api/tasks` against localhost:8000.
  [`task.service.ts:12`](../../frontend/src/app/services/task.service.ts#L12)

**Tests and runbook**

- API scenarios from the I/O matrix.
  [`test_tasks_api.py:4`](../../backend/tests/test_tasks_api.py#L4)

- Local run instructions for backend and frontend.
  [`README.md:9`](../../README.md#L9)
