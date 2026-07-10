

## Baseline Check

Before making feature changes, I ran:

`pytest -q`

Result:

`1 failed, 24 passed`

The failing test was:

`test_patch_same_status_returns_422`

The backend returned `200` for a same-status update. I kept this behavior because a user may edit other fields without changing the task status. I updated the test expectation to match the intended behavior.

---

## Backend Test Results

After Feature 1:

`29 passed`

After Feature 2:

`33 passed`

New tests covered:

- valid due dates
- invalid due-date format
- due-date updates
- overdue filtering
- search by title
- search by description
- combined filters
- empty search results

---

## Manual Browser Checks

I manually checked:

- creating a task with a due date
- editing a due date
- overdue indicator for past unfinished tasks
- no overdue indicator for Done tasks
- search by title
- search by description
- priority filtering
- overdue filtering
- combined search and filters
- empty Kanban columns staying visible
- drag and drop
- task deletion

All checks passed.

---

## Behavior Contract Before and After Changes

The following existing behavior was preserved:

- task creation
- task editing
- task deletion
- status transitions
- priority filtering
- Kanban columns
- drag and drop
- empty states

The final full test suite passed with:

`33 passed`

---

## Break Test Evidence

### Break Test 1

I temporarily changed the overdue rule so completed tasks with old due dates were included.

The overdue test failed because more than one task was returned.

I restored the rule:

- due date is before today
- status is not Done

The test passed again.

### Break Test 2

I temporarily changed search from case-insensitive matching to case-sensitive matching.

The title search test failed.

I restored lowercase comparison for both the search value and task text.

The test passed again.