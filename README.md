# Insurance Workflow — frontend demonstration

Six-page academic demo using Vite, plain HTML, CSS and JavaScript.
Initial scaffold only: all HTML bodies, shared CSS and shared JS are EMPTY.
There is no backend, real authentication, database or insurance processing.
Older SRS/SAD/test-plan files remain references, not delivered scope.
Current scope: docs/frontend-plan.txt; approved dates below supersede its old dates.

## Setup

Use Node.js 22.12 or newer. CI uses Node 22.

    npm ci
    npm run dev
    npm run build
    npm run preview

Open /index.html, /login.html, /dashboard.html, /application.html,
/applications.html and /staff.html. Initially each page is intentionally blank.
Build output must include all six pages. Build success verifies bundling,
not application features or simulated interactions.

## Ownership

- Anuj: scaffold, index.html, Jira, reviews, integration, charts and presentation.
- Renetta: login.html, dashboard.html, application.html, applications.html.
- Aswin: staff.html and agreed staff interactions.
- Raghav: css/style.css, js/main.js and manual frontend checks.

Coordinate shared-file edits with Raghav. Use only synthetic demo data.

## Branch and PR policy

1. Take an assigned Jira issue and acceptance criteria before coding.
2. Pull latest main, then create feat/IWM-12-login-page (use the actual key).
3. Edit assigned files; run npm run build and check affected pages in a browser.
4. Commit with the issue key, e.g. IWM-12: create login page; push the branch.
5. Open a PR with key, purpose, files, real results and screenshots once UI exists.
6. Anuj reviews teammates' changes. Another contributor reviews Anuj's changes.
7. Merge only after passing checks and review; no direct feature pushes to main.
8. Record actual Jira transitions: To Do, In Progress, In Review, Done.

If Anuj takes over missing work, record original owner, reassignment reason,
actual author and dates. Do not impersonate a teammate or invent approval.
Do not bypass branch review requirements to self-merge.

## Sprint plan

Sprint 1: 2–6 November 2026, Days 1–5: setup, page plans, landing/login,
dashboard, application form.
Sprint 2: 9–13 November 2026, Days 6–10: applications list, staff demo,
optional browser-only JS, integration and final presentation.
No mandatory weekend work. Record setup before sprint start as pre-sprint work.

## Evidence and charts

See docs/daily-evidence.md. Freeze estimates at actual sprint start.
Keep scope changes and reassignment visible. Final charts show genuine
planned/completed points, burndown, velocity and planned/actual Gantt.
Never backdate transitions or invent missing observations.
