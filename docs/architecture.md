# Architecture Context-Strategy Comparison Log

## Strategy comparison

| Strategy | What it got right | What it got wrong, missed, or invented | Best-suited task shape |
|---|---|---|---|
| **Strategy A — Minimal context** | Produced the broadest architecture view because it inspected the repository directly. It covered the app purpose, complete task model, create-task flow, backend, frontend, tests, dependencies, Docker context, and the mismatch between the README’s frontend path and the inspected path. It also separated confirmed facts from assumptions. | It depended on broad repository inspection, so it was less constrained and less repeatable than the other strategies. The draft also included more detail than the other versions and came closest to exceeding the one-page limit. The statement that the frontend refreshes after creation relied on interpreting the inspected frontend flow rather than runtime verification, although the draft disclosed that limit. | Best for an unfamiliar repository when the task needs a complete architecture overview and the reviewer is allowed to inspect widely. |
| **Strategy B — Structured context** | Preserved the important architecture facts while remaining concise: task fields, validation, FastAPI routes, JSON persistence, frontend/backend interaction, test-reset risk, and Module 5 governance. It used `AGENTS.md` and file summaries to organize the result consistently without reopening the whole repository. | It was only as reliable as the supplied summaries. It gave fewer evidence details than Strategy A, omitted the README/frontend path mismatch, and did not identify exact line references. Because no fresh files were inspected, stale or incomplete summaries could have carried into the architecture document. | Best for repeatable documentation tasks when a trusted `AGENTS.md` and accurate file summaries already exist. |
| **Strategy C — Targeted context** | Gave the clearest backend-only description of models, routes, and JSON persistence. It followed the scope restriction carefully and repeatedly marked excluded information as “not visible from the files I read,” which reduced unsupported claims. | It missed frontend behavior, tests, exact status-transition rules, dependency information, supported commands, Docker/CI context, and wider project purpose. Its “What the app does” section described mainly the API service rather than the full Task Tracker application because the frontend and README were outside the approved file set. | Best for a narrow backend question where the task depends mainly on models, route flow, and persistence, and where minimizing unrelated context is more important than full-system coverage. |

## Verdict

I would choose **Strategy B** for the final architecture document. It gives enough structured context to describe the whole application accurately while staying more concise and repeatable than Strategy A, and it avoids the major visibility gaps created by Strategy C. Strategy A remains the strongest choice when no trusted repository summary exists, but once `AGENTS.md` and accurate file summaries are available, Strategy B provides the best balance of coverage, control, and efficiency.

## Context-engineering rule

For a whole-application documentation task with a trusted repository guide and current file summaries, I use **Strategy B** because it provides broad coverage without requiring an unrestricted repository scan each time.

For a narrow backend behavior task that depends on only a few implementation files, I use **Strategy C** because its limited context makes unsupported assumptions easier to identify and label.
