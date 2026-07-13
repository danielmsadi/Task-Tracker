# Final AI Review and Ownership Evidence

## AGENTS.md guardrails

- Repo-specific stack and commands included: **yes**
- Docs-first/read-first guardrail included: **yes**
- Unexpected `app/` or `frontend/` edits rule included: **yes**
- Scope, secrets, verification, and ownership rules included: **yes**

The final-project layout moved the existing application folders from `backend/` to the required top-level `app/`, `frontend/`, and `tests/` paths. This was a documentation-supported release-structure correction required by the brief, not a product-feature change. No application or frontend behavior was intentionally changed.

## AI code review mini-log

Changed file reviewed: `.github/workflows/ci.yml`

| AI comment | Grade: Useful / Noise / Wrong | Reason | Verification or decision |
|---|---|---|---|
| Use an exact supported Python version instead of a vague or floating version. | Useful | The brief specifically asks for a non-vague Python version, and Docker already uses Python 3.11. | Accepted `python-version: "3.11"`; local tests passed on the available Python environment. |
| Add `continue-on-error: true` so documentation work is not blocked by test failures. | Wrong | This would hide a failed release check and is named as a dangerous shortcut in the brief. | Rejected. The pytest step fails the workflow normally. |
| Add pip dependency caching immediately. | Noise | Caching may improve speed, but it is not required evidence and adds configuration that is unnecessary for this small project. | Omitted to keep CI short and explainable. |

## AI security mini-review

| Finding | File evidence | Grade: Valid / False Positive / Noise | Reason | Next action |
|---|---|---|---|---|
| A local `.env` file was present in the uploaded working copy. | Pre-final `backend/.env`; final `.gitignore` and `.dockerignore` | Valid | The brief forbids `.env` files even when values appear harmless. | Removed the file and added repository/container ignore rules. |
| The tracked JSON file contained a local sample task and assignee value. | `data/tasks.json` | Valid | A public release should not include local or potentially personal task data. | Reset the release file to `{}` and documented that tests also reset it. |
| The API has no authentication and should receive a new auth system. | `app/main.py` | Noise | Authentication is explicitly outside this final project's scope, and adding it would be a new product feature. | No code change; keep the limitation visible and reject scope expansion. |
| `allow_headers=["*"]` is automatically a critical CORS vulnerability. | `app/main.py` local-origin CORS configuration | False Positive | The app restricts origins to the two local port-5500 development origins and does not enable credentials. The wildcard header setting alone does not prove a critical issue in this course context. | No change; reconsider only if deployment requirements change. |

## Manual security check

 The completed checks are recorded with exact results; only the online GitHub Actions result remains to be confirmed after pushing the final-project branch.

## One AI output I rejected or corrected

An AI suggestion to add authentication was rejected. It may be reasonable for a production application, but the final-project instructions explicitly prohibit adding authentication and require the existing Task Tracker to stay within course scope. The final work therefore documents the limitation instead of implementing a new feature.

## Three AI usage rules

1. Never paste: real secrets, `.env` values, tokens, credentials, production logs, or personal/customer data.
2. Always verify: inspect the diff, run the relevant command, and compare documentation claims with the actual repository or running app.
3. Record AI contributions by: naming the file or task, grading the suggestion, recording the decision, and keeping the evidence in `docs/`.

## Ownership statement

I am comfortable submitting this repository as my work because the final changes are limited to the required release structure, CI, Docker configuration, documentation, and data cleanup rather than a rewrite of the application. I can explain the run and test commands, the CI steps, the non-root Docker choice, and the evidence recorded in `docs/`. AI suggestions were reviewed and graded instead of accepted automatically, and out-of-scope suggestions such as authentication were rejected. The completed checks are recorded with exact results; only the online GitHub Actions result remains to be confirmed after pushing the final-project branch.
