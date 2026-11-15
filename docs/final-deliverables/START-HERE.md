# Insurance Workflow - final delivery pack

1. Open `Presentation-and-Speaking-Guide.pdf` for the presentation, speaking notes, two-minute live demo and viva questions.
2. Open `Final-SRS-SAD-Test-Plan.pdf` for the revised frontend specification, use-case/component/two sequence diagrams, requirements-to-tests traceability and deviation register.
3. Open `index.html` for charts and evidence. Keep full-size PNGs available for zooming.
4. Extract `source-eb232fb.zip` to a new folder to run the frozen application. Run `npm ci`, `npm run test:coverage`, `npm run build`, then `npm run dev`. Use Node 22.12 or newer. Source excludes dependencies and build output.

## What is complete

- PRs 36, 37 and 38 merged. PR38 reviewed by Renetta and merged at eb232fb0ff13fb5d2fc197b8b5d8526e01c7723b.
- Both Jira sprints closed. Sprint 2 integration issues IWM-33/34 Done; presentation issues IWM-36/37/38/39 remain incomplete in backlog.
- Actual-deadline charts and separate late-closeout chart, final timeline, CSV and raw Jira snapshots.
- Final application tests/build verified, selected-module coverage and actual screenshots preserved.

## What still requires people

- Independent review/merge of the new documentation publication PR.
- Team presentation (Anuj confirmed nobody has presented yet). Do not mark the four presentation tasks Done before that.
- Verify your assessor accepts the reduced frontend scope and screenshot-video format. If live narration/interaction is required, record the two-minute script while using the real website.
- Verify the separate linked GitHub Project requirement. Jira sprint evidence and GitHub issues/PRs are available; they do not by themselves prove a linked GitHub Project exists.

## Reporting rules

Deadline performance: Sprint 1 24/24 points, Sprint 2 16/32 points. Final closeout performance: Sprint 2 26/32 points. The remaining 6 points are presentation tasks. Do not substitute late completion for deadline performance.

Original October DOCX files inside the frozen source archive describe a proposed backend system. The revised PDF is the implementation baseline for this frontend release; original backend requirements are deferred, not silently passed.

## Reproducibility

`make_final.py` regenerates the charts and PDFs using the final JSON exports; it requires Python, matplotlib, reportlab and pymupdf. `build_charts.py` is a compatibility entry point for that generator. The earlier raw snapshots and `issue-history.csv` are historical pre-closeout evidence; use `issue-history-final.csv` for final status.

Screenshot videos: Sprint 1 60 seconds; Sprint 2 approximately 120 seconds. These are screenshot walkthroughs, not proof that teammates gave a live presentation.
