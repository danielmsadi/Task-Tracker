# Task Tracker Architecture

## 1. What the app does

The application is a FastAPI REST service for tracking tasks. It supports creating, listing, filtering, retrieving, partially updating, and deleting tasks, plus a health endpoint. A browser interface or other client is suggested by the configured local CORS origins, but the frontend itself is **not visible from the files I read** (`app/main.py:10-28`, `57-185`).

## 2. Data model

The main entity is `Task`, represented by three Pydantic models in `app/models.py`:

- `TaskCreate` — creation input
- `TaskUpdate` — optional fields for partial updates
- `TaskResponse` — complete stored and returned task

Important fields:

- `id`: server-generated string UUID
- `title`: required, trimmed, non-blank, maximum 200 characters
- `description`: optional during creation; stored as a string
- `status`: `ToDo`, `InProgress`, or `Done`
- `priority`: `Low`, `Medium`, or `High`
- `assignee`: optional string
- `due_date`: optional date
- `created_at` and `updated_at`: server-generated UTC datetimes

Unknown fields are forbidden in all three models (`app/models.py:8-78`).

## 3. Request flow: creating a task

1. A client sends JSON to `POST /tasks`.
2. FastAPI receives the body as a `TaskCreate` model.
3. The model applies field types, enum values, defaults, title trimming, blank-title rejection, the 200-character title limit, and rejection of unknown fields.
4. The route calls `storage.add_task(payload)`.
5. The storage layer generates a UUID and one UTC timestamp for both `created_at` and `updated_at`.
6. It creates a `TaskResponse`, adds it to an in-memory dictionary, and writes the full collection to `data/tasks.json`.
7. The route returns the created task with HTTP 201 (`app/main.py:57-80`; `app/storage.py:52-85`).

## 4. Key files

- `app/main.py` — FastAPI setup, CORS, health endpoint, and task CRUD/filter routes.
- `app/models.py` — task enums, request models, response model, defaults, and title validation.
- `app/storage.py` — in-memory task cache, filtering, CRUD operations, and JSON persistence.
- `app/business_rules.py` — imported by `main.py` to validate status changes; its internal rules are **not visible from the files I read**.
- `data/tasks.json` — JSON persistence path constructed by `storage.py`; its contents are **not visible from the files I read**.

## 5. Conventions

- **Validation:** Pydantic models define field types and reject extra fields. Status and priority use enums.
- **Storage:** Tasks are loaded into a process-local cache and persisted as a JSON object keyed by task ID.
- **Updates:** `PATCH` applies only supplied fields and generates a new UTC `updated_at`.
- **Status rules:** Status changes are passed to `validate_status_transition`; the exact allowed transitions are **not visible from the files I read**.
- **Error handling:** Missing task IDs produce HTTP 404 responses. Other global or unexpected-error handling is **not visible from the files I read**.
- **Frontend/backend interaction:** CORS permits `http://localhost:5500` and `http://127.0.0.1:5500`. The frontend implementation, request code, and user interface are **not visible from the files I read**.

## 6. Not visible or assumptions

The following are **not visible from the files I read**:

- Frontend structure and behavior
- Tests and expected test conventions
- Dependency versions and supported run commands
- Authentication, authorization, users, or task ownership
- Exact status-transition rules
- CI, container, or deployment configuration
- Production database or multi-process storage behavior
- Project-level instructions outside these three backend files
