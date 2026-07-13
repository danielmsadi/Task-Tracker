# Release Evidence

## Baseline

- Branch: `final-project`
- Date: 2026-07-13
- Local app run command: `python -m uvicorn app.main:app --reload --port 8000`
- `/health` result: HTTP 200 with `{"status":"ok","timestamp":"2026-07-13T14:42:07.848957+00:00"}`.
- Frontend run command: `python -m http.server 5500 --directory .\frontend`
- Frontend check: The Task Tracker Kanban board opened successfully. I created a temporary task, moved it from To Do to In Progress, tested the filters, and confirmed that the existing status-transition rules rejected moving it directly back to To Do. The temporary task was deleted after testing.
- Test command: `python -m pytest -q`
- Test result: `33 passed`.
- Scope result: No new product feature was added.
## Final verification


- Test command: `python -m pytest -q`
- Test result: `33 passed, 2 warnings in 0.35s` after the final release-only changes.
- API command: `python -m uvicorn app.main:app --host 127.0.0.1 --port 8765`
- `/health` result: HTTP 200 with `{"status":"ok","timestamp":"2026-07-13T14:17:05.454129+00:00"}`.
- Frontend command: `python -m http.server 8766 --directory frontend`
- Frontend result: HTTP 200; Kanban, Create Task, and Edit Task markers were present.
- Content-preservation check: SHA-256 comparison confirmed that the contents of `app/`, `frontend/index.html`, `tests/`, and `requirements.txt` were unchanged from the uploaded project; only their required release paths changed.

## CI evidence

- Workflow file: `.github/workflows/ci.yml`
- Trigger: The workflow runs on both `push` and `pull_request`.
- Python version: `3.11`.
- Dependency installation: `python -m pip install -r requirements.txt`
- Test command used by CI: `python -m pytest -q`
- Shortcut check: No `continue-on-error`, no `|| true`, and pytest is not skipped.
- Latest run link or note: Pending until the `final-project` branch is pushed to GitHub.



## Docker evidence

- Build command: `docker build -t task-tracker:final .`
- Build result: The image built successfully and was tagged `task-tracker:final`.
- Run command: `docker run --rm --name task-tracker-final -p 8000:8000 task-tracker:final`
- `/health` command: `curl.exe -i http://127.0.0.1:8000/health`
- `/health` result: `HTTP/1.1 200 OK`.
- Non-root check command: `docker image inspect task-tracker:final --format "{{.Config.User}}"`
- Non-root result: The command returned `app`, confirming that the container runs as a non-root user.
- No-baked-secrets check: I listed the files inside `/app` and confirmed that no `.env`, credentials, tokens, logs, or `.venv` files were included.
- Runtime command: `uvicorn app.main:app --host 0.0.0.0 --port 8000` is explicitly defined in the Dockerfile.

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| `python -m pytest -q` runs the complete test suite. | Ran the command in the project virtual environment. | Passed: `33 passed`. | No change needed. |
| `GET /health` responds successfully when the API is running. | Ran `curl.exe -i http://127.0.0.1:8000/health` against the local API. | Passed: `HTTP/1.1 200 OK`. | Updated the README to show the exact tested Windows command. |
| The Docker image builds and serves `/health`. | Built `task-tracker:final`, ran the container, and checked `/health`. | Passed: image built successfully and returned HTTP 200. | No change needed. |
| The Docker image runs as a non-root user. | Ran `docker image inspect task-tracker:final --format "{{.Config.User}}"`. | Passed: output was `app`. | No change needed. |
| The frontend command opens the Kanban application. | Ran `python -m http.server 5500 --directory frontend` from the repository root and opened the page in a browser. | Passed: the board, task controls, and filters were visible. | No change needed. |
