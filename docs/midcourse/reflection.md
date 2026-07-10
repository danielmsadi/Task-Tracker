During this mid-course project, I used AI tools as a coding assistant to help me plan, implement, test, and review changes to my Task Tracker application. I used AI mainly for brainstorming feature design, generating implementation suggestions, creating tests, and reviewing possible edge cases.

The first feature I implemented was Due Dates + Overdue Filtering. AI helped me decide how to keep the feature small by adding a due_date field to the existing task model instead of creating a new system. I reviewed the suggestions and kept the solution aligned with the project requirements by avoiding reminders, notifications, or unnecessary database changes.

The second feature was Search + Combined Filters. AI suggested different approaches, including more advanced search methods. After reviewing the options, I chose a simple case-insensitive search because it matched the size of the project and was easier to test and maintain.

One moment where AI helped was when writing pytest cases. It suggested scenarios I needed to verify, such as invalid dates, overdue filtering, and empty search results. These tests helped confirm the behavior instead of only checking the frontend manually.

One moment where AI slowed me down was when some suggestions were more complex than needed. Some ideas would have added extra endpoints or dependencies that were outside the project scope. I reviewed these suggestions and rejected the unnecessary complexity.

My own review changed the final result by keeping the architecture consistent with the existing Task Tracker. I kept JSON storage, reused the existing GET /tasks endpoint, and made sure the frontend changes matched the simple Kanban design.

This project showed me that AI is useful for speeding up development, but the developer still needs to understand the code, check assumptions, run tests, and decide which solutions actually fit the project.