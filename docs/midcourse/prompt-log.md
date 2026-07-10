# Prompt Log

## Feature 1: Due Dates + Overdue Filter

### Prompt 1
“You are a product owner. Create 3-5 user stories for optional due dates and overdue filtering in my FastAPI Task Tracker. Include acceptance criteria and stay within the current project scope.”

AI response:
Generated four user stories.

Decision:
Accepted them, but corrected the overdue rule so completed tasks are not overdue.

### Prompt 2
“You are a senior FastAPI developer. Suggest the smallest changes needed to add due dates using the current Pydantic models and JSON storage.”

AI response:
Suggested extending the existing models, API, storage, tests, and frontend.

Decision:
Accepted the small-change approach and rejected reminders, authentication, and database changes.

### Prompt 3
“Create pytest tests for valid due dates, invalid dates, updates, and overdue filtering using my existing test style.”

AI response:
Suggested focused backend tests.

Decision:
Accepted and adapted them to the project.

---

## Feature 2: Search + Combined Filters

### Prompt 1
“You are a product owner. Create 3-5 user stories for search and combined filters in my Task Tracker.”

AI response:
Generated four user stories.

Decision:
Accepted them, but corrected the assumption that empty Kanban columns should be hidden.

### Prompt 2
“You are a senior backend developer. Write a short ADR for keeping the existing FastAPI, Pydantic, JSON storage, pytest, and simple frontend architecture.”

AI response:
Claude generated an ADR with accepted and rejected alternatives.

Decision:
I shortened it and corrected technical details.

### Prompt 3
“Create pytest tests for title search, description search, combined filters, and empty results.”

AI response:
Suggested focused search tests.

Decision:
Accepted and adapted them.

---

## Weak Prompt Rewritten

Weak prompt:
“Add due dates and search.”

Why weak:
It did not include context, rules, or scope.

Improvement:
I added the AI role, project context, constraints, and expected output.