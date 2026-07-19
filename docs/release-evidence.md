# Release Evidence

## Evidence scope and finalization rule

- Branch: `final-project`
- Final evidence date: `2026-07-19`
- Evidence target: the exact final commit at the head of `final-project` when resubmitted.
- State rule: commit all corrections first, confirm `git status --short` is empty, then run the final tests and Docker checks and push that same commit. The GitHub Actions run must be green for that exact branch-head commit. Do not create another commit after these checks unless all final checks are repeated.
- This file records the commands, expected observations, and the rule used to tie the results to the submitted commit. The final verification is valid only when the repository is clean before the checks and no later commit is created.

## Local verification

- Local Python version: `3.12`.
- Local setup command: `python -m pip install -r requirements.txt`
- API run command: `python -m uvicorn app.main:app --reload --port 8000`
- `/health` check: `curl.exe -i http://127.0.0.1:8000/health`
- `/health` result: `HTTP/1.1 200 OK` with a JSON body containing `"status":"ok"` and a UTC timestamp.
- Frontend run command: `python -m http.server 5500 --directory frontend`
- Frontend result: the Kanban board and create/edit controls were visible; task movement rules and filters were manually exercised.
- Test command: `python -m pytest -q`
- Test result: `33 passed in 0.64s` using the local Python 3.12 virtual environment on `2026-07-19`.
- Release-version note: CI and Docker remain pinned to Python 3.11, as shown in `.github/workflows/ci.yml` and `Dockerfile`. The local Python 3.12 run is supporting verification, not a replacement for the release environment.
- Scope result: no new product feature was added.
- Application-change conclusion: `app/main.py`, `app/business_rules.py`, and `app/storage.py` received docstrings, but application behavior was preserved. The exact documentation-only changes are explained in `docs/final-ai-review.md`.

## CI evidence for the exact final commit

- Workflow file: `.github/workflows/ci.yml`
- Trigger: `push` and `pull_request`
- Python version: `3.11`
- Dependency installation: `python -m pip install -r requirements.txt`
- Test command used by CI: `python -m pytest -q`
- Shortcut check: no `continue-on-error`, no `|| true`, and pytest is not skipped.
- Exact-commit check: compare the commit SHA shown by the green GitHub Actions run with `git rev-parse HEAD` on `final-project`.
- Final result to record after push: the CI run is green for that SHA, and no later commit was added afterward.

## Docker evidence for the exact final commit

- Docker verification date: `2026-07-19`.
- Build command: `docker build -t task-tracker:final .`
- Run command: `docker run --rm --name task-tracker-final -p 8000:8000 task-tracker:final`
- `/health` check: `curl.exe -i http://127.0.0.1:8000/health`
- `/health` result: the container returned `{"status":"ok","timestamp":"2026-07-19T12:50:23.259452+00:00"}` with the Uvicorn response headers shown by `curl.exe -i`.
- Non-root check: `docker image inspect task-tracker:final --format "{{.Config.User}}"`
- Non-root result: `app`.
- No-baked-secrets check: `docker run --rm --entrypoint sh task-tracker:final -c "find /app -type f | sort"`; confirm that no `.env`, credentials, tokens, logs, or `.venv` files are included.
- No-baked-secrets result: `/app` contained only `app/__init__.py`, `app/business_rules.py`, `app/main.py`, `app/models.py`, `app/storage.py`, and `data/tasks.json`. No disallowed files were present.
- Runtime command: `uvicorn app.main:app --host 0.0.0.0 --port 8000` is explicitly defined in the Dockerfile.
- Exact-commit note: the remaining final commit changes only `README.md` and `docs/`, both excluded by `.dockerignore`; therefore they do not alter the Docker build context. CI must still run successfully for the final branch-head commit after it is pushed.

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| `python -m pytest -q` runs the complete test suite. | Full pytest run from the repository root using the local Python 3.12 virtual environment. | Passed: `33 passed in 0.64s` on `2026-07-19`. | CI and Docker stay pinned to Python 3.11 for release verification. |
| `GET /health` responds successfully. | Docker request using `curl.exe -i`. | Passed: a Uvicorn response with `{"status":"ok"}` and UTC timestamp at `2026-07-19T12:50:23.259452+00:00`. | Keep the exact tested Windows command in the release instructions. |
| The Docker image runs as a non-root user. | `docker image inspect task-tracker:final --format "{{.Config.User}}"`. | Passed: `app`. | No change needed. |
| The application source was unchanged. | Diff between `mid-course-project` and `final-project`. | Incorrect: docstrings were added in three `app/` files. | Corrected the claim to: application behavior was preserved, and the documentation-only edits are listed in `docs/final-ai-review.md`. |
| CI and Docker evidence represent the submitted state. | Clean branch-head commit, local Docker verification after that commit, and the GitHub Actions run for the same branch-head commit. | Valid only when the finalization rule above is followed. | Replaced conflicting historical statements with one internally consistent finalization rule. |
