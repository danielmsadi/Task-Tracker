# User Stories

## Feature 1: Due Dates + Overdue Filter

| ID | Story | Acceptance Criteria | Notes / Assumptions |
|---|---|---|---|
| DD-1 | As a team member, I want to add a due date to tasks when needed so that I can track deadlines for time-sensitive work. | - A task can be created with a due date.<br>- The due date accepts the YYYY-MM-DD format.<br>- A task without a due date remains valid. | due_date stays optional because the project already contains existing tasks without deadlines. |
| DD-2 | As a team member, I want to update a task due date so that I can change deadlines when task requirements change. | - A due date can be updated from the edit modal.<br>- The updated due date is saved after editing.<br>- Invalid date values are rejected by validation. | The existing update behavior should be extended instead of replaced. |
| DD-3 | As a team member, I want overdue tasks to have a visual indicator so that I can identify unfinished tasks past their deadline. | - A task is overdue when its due date is before today.<br>- Tasks with status Done are not marked overdue.<br>- Overdue tasks display an indicator on the task card. | **Corrected AI assumption:** AI initially treated completed tasks with old due dates as overdue. I corrected this because completed tasks should not appear as active overdue work. |
| DD-4 | As a team member, I want to filter tasks by overdue status so that I can view unfinished late tasks separately. | - An overdue filter is available.<br>- Only overdue tasks are returned when active.<br>- Empty Kanban columns remain visible. | Overdue filtering should reuse the existing task filtering system instead of adding a separate page. |

---

## Feature 2: Search + Combined Filters

| ID | Story | Acceptance Criteria | Notes / Assumptions |
|---|---|---|---|
| SF-1 | As a team member, I want to search tasks by title so that I can find specific tasks. | - Matching titles are returned.<br>- Partial text matches work.<br>- Search is case-insensitive. | Basic text search is enough because this is a small task tracker. |
| SF-2 | As a team member, I want search to include task descriptions so that I can find tasks using more details. | - Task descriptions are included in search.<br>- Matching descriptions return the related task.<br>- Empty descriptions do not cause errors. | No external search library is needed for this project scope. |
| SF-3 | As a team member, I want to combine search with existing filters so that I can narrow task results. | - Search works with status filtering.<br>- Search works with priority filtering.<br>- All active filters must match. | **Corrected AI assumption:** AI initially suggested returning tasks that match any selected filter. I corrected this so combined filters use AND logic. |
| SF-4 | As a team member, I want searches with no matches to return an empty board state so that the application behavior stays clear. | - No matches return an empty result.<br>- The request completes successfully without an error.<br>- Kanban columns remain visible. | Empty results are expected behavior and should not be handled as failures. |

**Corrected AI assumption:** AI initially treated completed tasks with old due dates as overdue. I corrected this because completed tasks should not appear as active overdue work.

**Corrected AI assumption:** AI initially suggested hiding Kanban columns when they had no matching tasks. I corrected this so all columns remain visible and show an empty state.