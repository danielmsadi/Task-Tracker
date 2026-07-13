# Personal AI Coding Playbook

## When I reach for AI first

I use AI first for bounded tasks such as explaining an unfamiliar file, drafting a test plan, checking documentation against code, reviewing a small diff, or listing risks before I make a change. I give it the exact task, allowed files, and expected evidence.During this course, AI was most useful when the answer could be verified with repository files, tests, or a command.

## When I do not reach for AI first

I do not ask AI to rewrite a project I have not read, make a high-risk change with missing context, or complete a learning exercise that I need to understand myself. I slow down when a task involves secrets, real user data, production access, destructive commands, or unclear permission. I first read the relevant files and ask for clarification when scope is uncertain.

## My non-negotiables

- I never paste real secrets, tokens, credentials, `.env` values, production logs, or personal/customer data.
- I confirm the allowed files and task scope before editing.
- I do not allow AI to push, deploy, delete data, or make external changes without my approval.
- I do not submit a line, command, configuration choice, or claim that I cannot explain.
- I do not hide failures with `continue-on-error`, `|| true`, skipped tests, or invented evidence.

## My review rules

I inspect the diff, connect each change to a requirement, and reject unrelated edits. I run the smallest useful verification first, then the full required tests. I check commands, endpoints, status codes, file paths, CI behavior, and Docker claims against the repository or a running app. I grade review comments as Useful, Noise, or Wrong and security findings as Valid, False Positive, or Noise. I record what I accepted, corrected, or rejected.

## What I am still figuring out

I am still learning when a team should use a fast AI review versus a deeper security scan, and how much AI evidence should be stored without making documentation too long. I will decide based on project risk, team rules, and whether the result can be reproduced by another developer.

## Decision Card

- New feature: read the requirement and existing design first; use AI for options and tests, not automatic implementation.
- Code review: ask for file-specific comments with evidence, then grade each comment.
- Debugging: reproduce the problem, collect the exact error, and ask AI about the smallest likely cause.
- Infrastructure: use exact versions and commands, then verify locally or in CI.
- Never paste: secrets, `.env` values, tokens, customer data, or production logs.
- One rule: AI may suggest; I must understand, verify, and own the final decision.
