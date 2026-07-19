# Final AI Review and Ownership Evidence

## AGENTS.md guardrails

- Repo-specific stack and commands included: **yes**
- Docs-first/read-first guardrail included: **yes**
- Unexpected `app/` or `frontend/` edits rule included: **yes**
- Scope, secrets, verification, and ownership rules included: **yes**

The final-project layout moved the existing application folders from `backend/` to the required top-level `app/`, `frontend/`, and `tests/` paths. This was a documentation-supported release-structure correction required by the brief, not a product-feature change. Application behavior was preserved.

## Documentation-only changes inside `app/`

The final-project diff was checked against the `mid-course-project` branch. Three application files contain documentation-only edits:

- `app/main.py`: docstrings were added or expanded for `health_check`, `create_task`, `list_tasks`, `get_task`, and `update_task`; a stray verification annotation was removed from the `create_task` docstring. The route decorators, endpoint paths, response models, status codes, parameters, validation calls, storage calls, and returned values were not changed.
- `app/business_rules.py`: a docstring was added to `validate_status_transition`. The `VALID_TRANSITIONS` set and the executable validation logic were not changed.
- `app/storage.py`: docstrings were added to `add_task`, `get_all_tasks`, `get_task_by_id`, `update_task`, and `delete_task`. The JSON persistence operations, filtering conditions, timestamps, identifiers, and return values were not changed.

These files were therefore not textually unchanged. The accurate conclusion is that their documentation changed while application behavior was preserved, which was verified by the existing test suite and runtime checks.

## Grader-requested validation correction

- `app/models.py`: creation requests now reject `null` for `description`, matching the existing non-null validation for `title`, `status`, and `priority`. Partial updates still allow these fields to be omitted, but explicitly sending `null` for any of the four fields is rejected with HTTP 422.
- `tests/test_tasks.py`: parametrized API tests cover all four fields for both create and patch requests.

This is a bounded data-integrity bug fix requested in the resubmission feedback. It does not add a feature or change the nullable behavior of `assignee` and `due_date`.

## AI code review mini-log

Changed file reviewed: `.github/workflows/ci.yml`

| AI comment | Grade: Useful / Noise / Wrong | Reason | Verification or decision |
|---|---|---|---|
| Use an exact supported Python version instead of a vague or floating version. | Useful | The brief specifically asks for a non-vague Python version, and Docker already uses Python 3.11. | Accepted `python-version: "3.11"`; the full test suite was used as verification. |
| Add `continue-on-error: true` so documentation work is not blocked by test failures. | Wrong | This would hide a failed release check and is named as a dangerous shortcut in the brief. | Rejected. The pytest step fails the workflow normally. |
| Add pip dependency caching immediately. | Noise | Caching may improve speed, but it is not required evidence and adds unnecessary configuration for this small project. | Omitted to keep CI short and explainable. |

## AI security mini-review

| Finding | File evidence | Grade: Valid / False Positive / Noise | Reason | Next action |
|---|---|---|---|---|
| A local `.env` file was present in the original working copy. | Pre-final `backend/.env`; final `.gitignore` and `.dockerignore` | Valid | The brief forbids `.env` files even when values appear harmless. | The file was removed and ignore rules were added. |
| The tracked JSON file contained a temporary task and assignee-related field. | `data/tasks.json` | Valid | A public release should not contain temporary or potentially personal task data. | The release file was reset to `{}`. |
| The API has no authentication and should receive a new authentication system. | `app/main.py` | Noise | Authentication is explicitly outside this final project's scope and would add a product feature. | No code change; the suggestion was rejected. |
| `allow_headers=["*"]` is automatically a critical CORS vulnerability. | `app/main.py` local-development CORS configuration | False Positive | Allowed origins are restricted to the two local frontend origins and credentials are not enabled. The wildcard header setting alone does not establish a critical vulnerability in this local course configuration. | No change; reassess only if deployment requirements change. |

## Manual security check

I personally opened and reviewed `.gitignore`, `.dockerignore`, `Dockerfile`, and `data/tasks.json` instead of relying only on the AI review. I confirmed that `.env` files, virtual environments, caches, and logs are excluded; `data/tasks.json` contains only `{}`; and the Dockerfile copies `requirements.txt`, `app/`, and `data/` rather than copying the full repository. I also checked the tracked-file list with `git ls-files` for `.env`, key, credential, and secret filenames, and searched the working tree (excluding Git metadata and virtual environments) for secret-assignment markers. Neither check produced a finding. The Docker container file-list check was also completed: `/app` contained only the application files and `data/tasks.json`, with no `.env`, credentials, tokens, logs, or virtual environment files. This matters because the public GitHub repository and the Docker build context can be inspected by another developer, so local or sensitive information must not be exposed.

## One AI output I rejected or corrected

An AI suggestion to add authentication was rejected. Authentication may be reasonable for a production application, but the final-project instructions explicitly prohibit adding it and require the existing Task Tracker to stay within course scope. The final work documents the limitation instead of implementing a new feature.

I also corrected an earlier AI-generated claim that `app/` was unchanged. The diff showed that docstrings had been added, so the final evidence now states the narrower and accurate conclusion: documentation changed, but application behavior was preserved.

## Three AI usage rules

1. Never paste: real secrets, `.env` values, tokens, credentials, production logs, or personal/customer data.
2. Always verify: inspect the diff, run the relevant command, and compare documentation claims with the actual repository or running app.
3. Record AI contributions by: naming the file or task, grading the suggestion, recording the decision, and keeping the evidence in `docs/`.

## Ownership statement

I am comfortable submitting this repository as my work because I reviewed the final diff and can explain the release structure, CI workflow, Docker configuration, documentation changes, and data cleanup. I understand that `app/main.py`, `app/business_rules.py`, and `app/storage.py` received docstrings, while their executable behavior was preserved. I verified AI suggestions instead of accepting them automatically and rejected changes that would expand the project scope or hide failures. The final CI and Docker checks are tied to the exact resubmission commit as recorded in `docs/release-evidence.md`, and no later commit should be submitted without repeating those checks.
