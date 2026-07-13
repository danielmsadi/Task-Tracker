# Task Tracker Architecture

## 1. What the app does

Task Tracker is a small learning application for managing tasks through a browser-based Kanban board. Users can create, view, update, delete, search, filter, and move tasks between **To Do**, **In Progress**, and **Done**. A FastAPI backend validates requests and stores task records in a local JSON file.

## 2. Data model

The main entity is `Task`.

Important fields:

- `id`: server-generated UUID string
- `title`: required, trimmed, non-empty, maximum 200 characters
- `description`: string
- `status`: `ToDo`, `InProgress`, or `Done`
- `priority`: `Low`, `Medium`, or `High`
- `assignee`: optional string
- `due_date`: optional date
- `created_at`: server-generated UTC datetime
- `updated_at`: server-generated UTC datetime

The backend separates create, partial-update, and response models. Unknown request fields are rejected.

## 3. Request flow

When a user creates a task:

1. The user completes the task form in the browser frontend.
2. Frontend JavaScript sends a JSON request to `POST /tasks`.
3. FastAPI parses the request through the task creation model.
4. Pydantic validates the field types, title rules, enums, and unknown fields.
5. The route passes the validated task data to the storage layer.
6. The storage layer generates the UUID and UTC timestamps.
7. The new task is added to the in-memory task collection and written to `data/tasks.json`.
8. The API returns the created task with HTTP 201.
9. The frontend refreshes the task list and redraws the board.

## 4. Key files

- `AGENTS.md` — repository instructions, confirmed commands, Module 5 guardrails, and governance rules.
- `README.md` — project summary, setup steps, API routes, and development notes.
- `app/models.py` — task enums, validation, request models, and response model.
- `app/main.py` — FastAPI setup, CORS configuration, health endpoint, and task routes.
- `app/business_rules.py` — permitted task-status transitions.
- `app/storage.py` — task loading, filtering, creation, updates, deletion, and JSON persistence.
- `frontend/index.html` — complete HTML, CSS, and JavaScript frontend.
- `tests/conftest.py` — shared test fixtures and storage reset behavior.
- `tests/test_tasks.py` — tests for validation, filtering, CRUD behavior, and transitions.
- `requirements.txt` — pinned Python dependencies.

## 5. Conventions

- **Validation:** Pydantic models validate request data. Status and priority use enums, task titles are trimmed and limited, and extra fields are forbidden.
- **Storage:** Tasks are cached in memory and persisted in `data/tasks.json`.
- **Updates:** `PATCH` changes only fields included in the request and refreshes `updated_at`.
- **Business rules:** Status transitions are validated before updates are saved.
- **Errors:** Missing tasks return HTTP 404. Invalid request data or status transitions return HTTP 422.
- **Frontend/backend interaction:** The frontend makes HTTP requests to the FastAPI backend and displays loading, empty, success, and error states.
- **Testing:** pytest uses shared fixtures, but the current reset behavior clears the normal JSON data file and must be treated carefully.

## 6. Not visible or assumptions

- Authentication, authorization, user accounts, and task ownership are not visible.
- A production database, queue, cache service, or external API is not visible.
- Automated frontend testing is not visible.
- CI configuration is not visible in the current repository context.
- Production scaling, availability, and deployment requirements are not confirmed.
- The application is treated as a learning project rather than a confirmed production system.
