# ADR: Due Dates + Overdue Filter, Search + Combined Filters

## Status
Accepted

## Context
The Task Tracker already supports create, view, update, delete, status/priority filtering, and moving tasks between Kanban columns, using FastAPI, Pydantic, JSON file storage, pytest, and a plain HTML/CSS/JS frontend.

For this mid-course checkpoint, two features are being added:

1. Due dates on tasks, with an overdue filter.
2. Search by title/description, combined with the existing filters.

This is a learning project. The goal is to add these features with the smallest changes possible, without introducing new architecture, libraries, or infrastructure.

## Decision
Keep the existing stack as-is and extend it directly:

- Add an optional `due_date` field to the `Task` Pydantic model, stored as a string in `YYYY-MM-DD` format. It can be set on create or on partial update.
- A task is considered overdue if `due_date` is before today's date **and** its status is not `Done`.
- Extend the existing `GET /tasks` endpoint with an `overdue` query parameter, rather than creating a separate endpoint.
- Add a `search` query parameter to `GET /tasks` that checks both `title` and `description`, case-insensitively, using simple substring matching (no external search library).
- All filters (`status`, `priority`, `overdue`, `search`) combine with AND logic — a task must match every active filter to be included.
- On the frontend, overdue tasks get a visual indicator (e.g. a CSS class), and Kanban columns always render even when empty, showing an empty-state message instead of disappearing.

## Alternatives Considered
- **Separate `/tasks/overdue` and `/tasks/search` endpoints** — rejected to avoid duplicating filter logic; extending `GET /tasks` keeps filtering in one place.
- **Storing `due_date` as a Python `date`/`datetime` object** — rejected for this stage; keeping it as a plain string keeps JSON serialization simple and consistent with the rest of the storage layer.
- **OR logic between filters** — considered for search, but AND logic matches how the existing status/priority filters already behave and is easier to reason about.

## Accepted AI Suggestions
- Add `due_date` as an optional field usable on both create and partial update.
- Extend `GET /tasks` with new query parameters instead of adding new routes.
- Case-insensitive, partial-match search over title and description.
- AND logic across all combined filters.

## Rejected AI Suggestions
- AI initially treated tasks with a past due date as overdue regardless of status. Corrected so tasks with status `Done` are never overdue, since a finished task isn't "late."
- AI initially suggested hiding Kanban columns with no matching tasks. Corrected so all columns stay visible with an empty state, so the board layout doesn't shift around while filtering/searching.

## Consequences
- `Task` model, JSON storage, and `GET /tasks` need small updates; no new files or layers are required.
- Existing tasks without a `due_date` remain valid since the field is optional.
- Filter logic in `GET /tasks` grows a bit more complex as more query parameters are added, but stays in one place rather than being spread across endpoints.
- No authentication, accounts, notifications, database, or frontend framework are introduced — scope stays limited to the two selected features.