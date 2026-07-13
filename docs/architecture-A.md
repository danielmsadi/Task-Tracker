# Task Tracker Architecture

## 1. What the app does

Task Tracker is a small learning application for creating and managing tasks on a browser-based Kanban board. Users can create, view, edit, delete, search, filter, and drag tasks between **To Do**, **In Progress**, and **Done**. A FastAPI backend validates requests and stores task records in a local JSON file (`README.md:1-20`; `frontend/index.html:869-1015`).

## 2. Data model

The main entity is `Task`, represented by Pydantic models in `app/models.py`.

Important fields:

- `id`: server-generated UUID string
- `title`: required, trimmed, non-blank, maximum 200 characters
- `description`: string; defaults to empty
- `status`: `ToDo`, `InProgress`, or `Done`
- `priority`: `Low`, `Medium`, or `High`
- `assignee`: optional string
- `due_date`: optional date
- `created_at`: server-generated UTC datetime
- `updated_at`: server-generated UTC datetime

`TaskCreate` defines creation input, `TaskUpdate` supports partial updates, and `TaskResponse` defines persisted and returned records. Unknown request fields are rejected (`app/models.py:8-78`).

## 3. Request flow: creating a task

1. The user completes the task form in `frontend/index.html`.
2. Browser JavaScript sends a JSON `POST /tasks` request to the backend.
3. FastAPI parses the body as `TaskCreate`; Pydantic applies enum, type, title, and unknown-field validation.
4. `create_task()` passes the validated model to `storage.add_task()` (`app/main.py:57-80`).
5. The storage layer generates a UUID and UTC timestamps, builds a `TaskResponse`, adds it to the in-memory task cache, and rewrites `data/tasks.json` (`app/storage.py:52-85`).
6. FastAPI serializes the created task and returns HTTP 201.
7. The frontend reloads the task collection and redraws the Kanban board.

## 4. Key files

- `AGENTS.md` — AI-working rules, confirmed commands, project guardrails, and repository notes.
- `README.md` — project purpose, setup instructions, routes, and development overview.
- `app/models.py` — task enums, request models, response model, defaults, and title validation.
- `app/main.py` — FastAPI configuration, CORS settings, health route, and task CRUD routes.
- `app/business_rules.py` — permitted task-status transitions and invalid-transition errors.
- `app/storage.py` — in-memory cache, filtering, UUID/timestamp creation, and JSON persistence.
- `frontend/index.html` — complete HTML, CSS, and JavaScript Kanban frontend.
- `tests/conftest.py` — shared API client and automatic storage-reset fixtures.
- `tests/test_tasks.py` — validation, filtering, CRUD, due-date, search, and transition tests.
- `requirements.txt` — pinned backend and test dependencies.

## 5. Conventions

- **Validation:** Pydantic validates API input. Status and priority use enums, titles are trimmed and limited, and extra fields are forbidden.
- **Storage:** Tasks are cached in memory and persisted as a JSON object keyed by task ID in `data/tasks.json`.
- **Updates:** `PATCH` applies only supplied fields and refreshes `updated_at`.
- **Business rules:** Status changes are checked before storage updates; invalid changes return HTTP 422.
- **Errors:** Missing task IDs return HTTP 404 with a readable `detail` message. Invalid request data is handled by FastAPI/Pydantic.
- **Frontend/backend interaction:** The frontend calls `http://localhost:8000`, while backend CORS permits the local port-5500 frontend origins (`app/main.py:16-28`; `frontend/index.html:582-583`).
- **Testing:** pytest uses FastAPI’s `TestClient`; current fixtures reset the normal JSON task file before and after tests.

## 6. Not visible or assumptions

- Authentication, authorization, user accounts, and task ownership are not visible.
- A production database, background jobs, message queues, and external services are not visible.
- CI configuration and deployment infrastructure beyond the `Dockerfile` are not visible.
- No frontend framework, build process, or automated browser-test setup is visible.
- The repository is described as a learning project, so production scaling and availability requirements are not confirmed.
- The final-project release layout now uses the required top-level `frontend/index.html` path; the original review found the same file under `backend/` before the release-layout correction.
