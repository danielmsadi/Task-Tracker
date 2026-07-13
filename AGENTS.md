# AGENTS.md

## Purpose

This file defines the rules for AI-assisted work in the Task Tracker repository. The final-project goal is release checking, documentation, review, and governance. It is not permission to add product features.

## Confirmed stack and paths

- Python 3.11
- FastAPI, Pydantic, and Uvicorn
- pytest and HTTPX
- Plain HTML, CSS, and JavaScript
- Local JSON persistence
- `app/` - API, models, business rules, and storage
- `data/tasks.json` - local task data
- `frontend/index.html` - Kanban frontend
- `tests/` - pytest suite
- `.github/workflows/ci.yml` - CI workflow
- `Dockerfile` and `.dockerignore` - container release files
- `docs/` - course evidence and decisions

## Confirmed commands

Install dependencies from the repository root:

```powershell
python -m pip install -r requirements.txt
```

Run the API:

```powershell
python -m uvicorn app.main:app --reload --port 8000
```

Run the frontend:

```powershell
python -m http.server 5500 --directory frontend
```

Run the tests:

```powershell
python -m pytest -q
```

Build and run Docker:

```powershell
docker build -t task-tracker:final .
docker run --rm --name task-tracker-final -p 8000:8000 task-tracker:final
curl.exe -i http://127.0.0.1:8000/health
```

## Read-first and docs-first guardrails

1. Read the assignment, `README.md`, this file, and the relevant source or test files before proposing a change.
2. Start with read-only inspection and state which files support each repository claim.
3. For final-project work, prefer changes to `README.md`, `AGENTS.md`, `.github/`, Docker files, and the required `docs/` evidence.
4. Update documentation before changing application behavior when a documentation correction is enough.
5. Do not invent commands, endpoints, tools, test results, GitHub links, or Docker results.

## Scope rules

- Do not add comments, authentication, a production database, notifications, or unrelated UI changes.
- Do not rewrite the application.
- Do not modify `app/` or `frontend/` unless a small bug fix, security fix, or documentation-supported correction is explicitly required.
- Any unexpected `app/` or `frontend/` edit must stop the task for review and must be explained in `docs/final-ai-review.md`.
- The final layout move to top-level `app/`, `frontend/`, and `tests/` is a documentation-supported release correction required by the final-project brief; no product logic was added.
- Keep each AI task bounded. Do not mix feature work with release evidence.

## Data and security rules

- Never paste or commit real secrets, tokens, credentials, `.env` files, production logs, or personal/customer data.
- Treat local task data as disposable course data. Keep `data/tasks.json` empty in the public release.
- Do not weaken CI with `continue-on-error`, `|| true`, a skipped pytest command, or an unspecified Python version.
- Do not copy `.env` files or the full repository into the Docker image.
- Prefer explicit file copies and a non-root runtime user in Docker.

## Verification rules

- Run `python -m pytest -q` and record the exact result.
- Start the API and verify `GET /health` returns HTTP 200.
- Serve `frontend/` and confirm the Kanban board and create/edit flow remain present.
- Build and run Docker before submission in an environment that has Docker, then verify `/health` returns HTTP 200.
- Inspect the final diff and secret scan before committing.
- If a check cannot be run, mark it as not verified and do not replace it with an assumption.

## AI review and ownership rules

- Grade AI review comments as Useful, Noise, or Wrong with a reason.
- Grade security findings as Valid, False Positive, or Noise with file evidence.
- Reject AI output that adds scope, hides failures, changes unrelated code, or cannot be explained.
- Record one manual check that is separate from the AI review.
- The person submitting the repository must understand every final command, config choice, and changed line.
