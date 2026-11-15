# Insurance Workflow — frontend demonstration

Six-page academic demo using Vite, plain HTML, CSS and JavaScript.
All six pages are implemented. Applicant forms show no-save confirmations; staff actions update only the selected card and reset on refresh.
The original blank scaffold was preserved in merged PR #13.
There is no backend, real authentication, database or insurance processing.
Older SRS/SAD/test-plan files remain references, not delivered scope.
Current scope: docs/frontend-plan.txt; approved dates below supersede its old dates.

## Setup

Use Node.js 22.12 or newer. CI uses Node 22.

    npm ci
    npm run dev
    npm run test:coverage
    npm run build
    npm run preview

Open /index.html, /login.html, /dashboard.html, /application.html,
/applications.html and /staff.html. All six routes contain demo content.
Build output must include all six pages. Build success verifies bundling,
not application features or simulated interactions.

## Ownership

- Anuj: scaffold, index.html, Jira, reviews, integration, charts and presentation.
- Renetta: login.html, dashboard.html, application.html, applications.html.
- Aswin: staff.html and agreed staff interactions.
- Raghav: css/style.css, js/main.js and manual frontend checks.

On 2 November, Anuj took over missing Day 3 prerequisites and Day 4–5 work
(IWM-13 through IWM-20). Original ownership remains above and in Jira history;
the actual implementation is credited to Anuj. See docs/evidence/2026-11-02.

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
Sprint 2 actually started early on 7 November. Late closeout work on 15 November is reported separately from the original 13 November deadline.
No mandatory weekend work. Record setup before sprint start as pre-sprint work.

## Evidence and charts

See docs/daily-evidence.md. Freeze estimates at actual sprint start.
Keep scope changes and reassignment visible. Final charts show genuine
planned/completed points, burndown, velocity and planned/actual Gantt.
Never backdate transitions or invent missing observations.

Sprint 1 design, scope deviations and test results:
[design and validation record](docs/sprint-1-design-and-validation.md).

## Final delivery and presentation (15 November 2026)

The frozen application baseline is `eb232fb0ff13fb5d2fc197b8b5d8526e01c7723b` (PR #38, independently approved by Renetta). Both Jira sprints are closed; the four presentation tasks remain incomplete in backlog because the team has not presented yet.

Start with [the delivery guide](docs/final-deliverables/START-HERE.md), [presentation PDF](docs/final-deliverables/Presentation-and-Speaking-Guide.pdf), and [final SRS/SAD/Test Plan](docs/final-deliverables/Final-SRS-SAD-Test-Plan.pdf). The final PDF reconciles this frontend-only release with the original October DOCX proposal; it does not claim delivery of the proposed backend or formal IEEE certification. Documentation acceptance remains subject to review.

[Chart provenance](docs/final-deliverables/CHART-NOTES.md) distinguishes original-deadline completion (24/24 and 16/32 points) from late Sprint 2 closeout (26/32). Six presentation points are still incomplete. The 60-second and approximately 120-second videos are screenshot walkthroughs, not proof of a live team presentation.
