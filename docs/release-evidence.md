# Release Evidence

## Evidence scope and finalization rule

- Branch: `final-project`
- Final evidence date: `2026-07-19`
- Evidence target: correction commit `84d3f198c6ebde3be4d467c49ed22ef6b6a8e602` on `final-project`.
- State rule: the application correction, its regression tests, and the supporting documentation were committed together, pushed, and verified by GitHub Actions. The later evidence-only commit records that observed result and does not change application code, tests, dependencies, Docker inputs, or CI configuration.
- This file ties the successful CI result directly to the commit containing the grader-requested null-validation correction.

## Local verification

- Local Python version: `3.12`.
- Local setup command: `python -m pip install -r requirements.txt`
- API run command: `python -m uvicorn app.main:app --reload --port 8000`
- `/health` check: `curl.exe -i http://127.0.0.1:8000/health`
- `/health` result: `HTTP/1.1 200 OK` with a JSON body containing `"status":"ok"` and a UTC timestamp.
- Frontend run command: `python -m http.server 5500 --directory frontend`
- Frontend result: the Kanban board and create/edit controls were visible; task movement rules and filters were manually exercised.
- Test command: `python -m pytest -q`
- Test result: `41 passed in 0.68s` using the local virtual environment on `2026-07-19` after the grader-requested null-validation correction.
- Release-version note: CI and Docker remain pinned to Python 3.11, as shown in `.github/workflows/ci.yml` and `Dockerfile`. The local Python 3.12 run is supporting verification, not a replacement for the release environment.
- Scope result: no new product feature was added.
- Application-change conclusion: `app/models.py` received the bounded data-integrity correction requested by the grader, and `tests/test_tasks.py` received regression coverage. The earlier documentation-only source changes remain explained in `docs/final-ai-review.md`.

## CI evidence for the exact final commit

- Workflow file: `.github/workflows/ci.yml`
- Trigger: `push` and `pull_request`
- Python version: `3.11`
- Dependency installation: `python -m pip install -r requirements.txt`
- Test command used by CI: `python -m pytest -q`
- Shortcut check: no `continue-on-error`, no `|| true`, and pytest is not skipped.
- Exact-commit check: compare the run's `head_sha` with `git show -s --format=%H 84d3f19` and confirm that commit contains the application and regression-test correction.
- Submitted correction commit SHA: `84d3f198c6ebde3be4d467c49ed22ef6b6a8e602`.
- Final successful correction run: GitHub Actions CI run `#12`, `https://github.com/danielmsadi/Task-Tracker/actions/runs/29693659216`.
- Result: `completed` with conclusion `success` on `2026-07-19`.
- Confirmation: the run's `head_sha` is `84d3f198c6ebde3be4d467c49ed22ef6b6a8e602`, exactly matching the commit containing the `app/models.py` correction and null-validation regression tests.

## Docker evidence for the exact final commit

- Current correction status: rebuilt and reverified from the corrected working tree on `2026-07-19`. Repeat only if Docker inputs change before the final commit.
- Docker verification date: `2026-07-19`.
- Build command: `docker build -t task-tracker:final .`
- Run command: `docker run --rm --name task-tracker-final -p 8000:8000 task-tracker:final`
- `/health` check: `curl.exe -i http://127.0.0.1:8000/health`
- `/health` result: the rebuilt final image returned HTTP 200 with `{"status":"ok","timestamp":"2026-07-19T15:47:30.802224+00:00"}`.
- Non-root check: `docker image inspect task-tracker:final --format "{{.Config.User}}"`
- Non-root result: `app`.
- No-baked-secrets check: `docker run --rm --entrypoint sh task-tracker:final -c "find /app -type f | sort"`; confirm that no `.env`, credentials, tokens, logs, or `.venv` files are included.
- No-baked-secrets result: `/app` contained only `app/__init__.py`, `app/business_rules.py`, `app/main.py`, `app/models.py`, `app/storage.py`, and `data/tasks.json`. No disallowed files were present.
- Runtime command: `uvicorn app.main:app --host 0.0.0.0 --port 8000` is explicitly defined in the Dockerfile.
- Exact-commit procedure: after this final cleanup commit is created, rebuild and check the image from its Docker inputs: `Dockerfile`, `.dockerignore`, `requirements.txt`, `app/`, and `data/`. Do not create a later commit after that Docker check; CI then verifies the exact final branch-head commit after push.

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| `python -m pytest -q` runs the complete test suite. | Full pytest run from the repository root using the local virtual environment. | Passed: `41 passed in 0.68s` on `2026-07-19` after the null-validation correction. | CI and Docker stay pinned to Python 3.11 for release verification. |
| Core task fields reject explicit `null`. | Parametrized POST and PATCH API tests for `title`, `description`, `status`, and `priority`. | Passed: all eight cases returned HTTP 422 as part of the 41-test run. | `app/models.py` keeps partial-update omission valid while rejecting explicit nulls. |
| `GET /health` responds successfully. | Docker request using `curl.exe -i` against the rebuilt final image. | Passed: `HTTP/1.1 200 OK` with `{"status":"ok"}` and UTC timestamp at `2026-07-19T13:48:04.231512+00:00`. | Keep the exact tested Windows command in the release instructions. |
| The Docker image runs as a non-root user. | `docker image inspect task-tracker:final --format "{{.Config.User}}"`. | Passed: `app`. | No change needed. |
| The application source was unchanged. | Diff between `mid-course-project` and `final-project`. | Incorrect: docstrings were added in three `app/` files. | Corrected the claim to: application behavior was preserved, and the documentation-only edits are listed in `docs/final-ai-review.md`. |
| CI and Docker evidence represent the submitted state. | Clean branch-head commit, local Docker verification after that commit, and the GitHub Actions run for the same branch-head commit. | Valid only when the finalization rule above is followed. | Replaced conflicting historical statements with one internally consistent finalization rule. |
