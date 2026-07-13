# Task Tracker

Task Tracker is a lightweight learning application built with Python, FastAPI, Pydantic, plain HTML, CSS, and JavaScript. It provides a Kanban interface and a REST API for creating, viewing, filtering, updating, moving, and deleting tasks. Task data is stored in a local JSON file.

## Features

- Create, read, update, and delete tasks.
- Track status, priority, assignee, and due date.
- Search tasks and filter by priority or overdue state.
- Move tasks between To Do, In Progress, and Done.
- Persist task data in `data/tasks.json`.
- Check service availability through `GET /health`.

## Repository structure

```text
.github/workflows/ci.yml
Dockerfile
.dockerignore
README.md
AGENTS.md
requirements.txt
app/
data/
frontend/
tests/
docs/
```

## Requirements

- Python 3.11 is the verified release version.
- `pip` for installing dependencies.
- Docker only for the container workflow.

## Local setup

Run these commands from the repository root.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run the application locally

Start the API from the repository root:

```powershell
python -m uvicorn app.main:app --reload --port 8000
```

The API is available at `http://127.0.0.1:8000`, the Swagger UI is at `http://127.0.0.1:8000/docs`, and the health endpoint is at `http://127.0.0.1:8000/health`.

In a second terminal, start the frontend:

```powershell
python -m http.server 5500 --directory frontend
```

Open `http://127.0.0.1:5500` in a browser.

## Run the tests

From the repository root:

```powershell
python -m pytest -q
```

The test fixture resets `data/tasks.json`, so do not keep important local task data in that file while running the suite.

## Run with Docker

Build the image:

```powershell
docker build -t task-tracker:final .
```

Run the container:

```powershell
docker run --rm --name task-tracker-final -p 8000:8000 task-tracker:final
```

Check the container from another terminal:

```powershell
curl.exe -i http://127.0.0.1:8000/health
```

Stop it with `Ctrl+C`. The image runs the API as a non-root user and copies only the application package and empty local data file into the runtime image.

## API endpoints

| Method | Route | Purpose |
| --- | --- | --- |
| GET | `/health` | Return service status and a UTC timestamp. |
| POST | `/tasks` | Create a task. |
| GET | `/tasks` | List tasks with optional filters. |
| GET | `/tasks/{task_id}` | Get one task. |
| PATCH | `/tasks/{task_id}` | Partially update a task. |
| DELETE | `/tasks/{task_id}` | Delete a task. |

## Final Project

Branch reviewed: `final-project`

### What this submission demonstrates

- The existing Task Tracker still runs inside the intended course scope.
- CI runs the pytest suite on push and pull request.
- The Docker configuration uses a clear runtime command and a non-root user.
- AI review, security, release, and ownership evidence is stored in `docs/`.
- No new product feature was added for the final project.

### How to run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

In a second terminal:

```powershell
python -m http.server 5500 --directory frontend
```

### How to run tests

```powershell
python -m pytest -q
```

### How to run with Docker

```powershell
docker build -t task-tracker:final .
docker run --rm --name task-tracker-final -p 8000:8000 task-tracker:final
curl http://127.0.0.1:8000/health
```

### Evidence files

- `docs/release-evidence.md`
- `docs/final-ai-review.md`
- `docs/ai-playbook.md`

### AI assistance summary

AI helped review the repository, prepare the required release files, check documentation claims, and perform a read-only security review. The work was verified with pytest, a local API health request, a served frontend check, Docker runtime verification, and a check of the files included in the Docker image. Suggestions that would add out-of-scope product features or hide failures were rejected.
