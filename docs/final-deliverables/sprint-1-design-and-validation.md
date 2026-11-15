# Sprint 1 design and validation record

Prepared by Anuj on 3 November 2026. Covers IWM-10, IWM-11, IWM-12 and
the implementation IWM-13–20. This records actual work, not teammate authorship.

## Scope deviation from the original backend plan

The user-approved frontend-only plan supersedes backend implementation for
these two sprints. Original SRS/SAD documents remain historical references.
This increment demonstrates interface flow only: no authentication, database,
document uploads, insurer decisions, audit service or real submission exists.
Those original requirements are not satisfied by this demo. Final IEEE-format
documents must explicitly reconcile this deviation before the final assessment.

## Page and navigation plan (IWM-10)

| Page | Sprint | Purpose and exits |
| --- | --- | --- |
| index.html | 1 | Explain demo; link to login and clearly labelled planned staff route |
| login.html | 1 | Fictional required username/password; validate only; separate dashboard link |
| dashboard.html | 1 | Static demo overview; new application and planned applications route |
| application.html | 1 | Name, insurance type, contact email and requested INR amount; return to dashboard |
| applications.html | 2 | Planned synthetic applications list; currently blank scaffold |
| staff.html | 2 | Planned staff interface; currently blank scaffold |

Application name is required, maximum 100 characters. Insurance type is a
required choice of health, vehicle or home. Email must satisfy browser email
validation. Amount is a required positive whole number. Successful validation
shows a notice that nothing was sent or saved; editing clears that notice.
Inputs are not inserted as HTML, stored, or sent to a service. Use fictional data.

## Staff plan (IWM-11 and IWM-17)

See [staff-page-outline.md](staff-page-outline.md) for fields and status labels.
The future view has a synthetic list, selected details and clearly labelled demo
decision controls. It shares applicant field terminology and CSS. A selection
must be visible before a future decision control is enabled. No real staff
authorization or insurance decision is implied. Day 8 behavior remains optional.

## Visual conventions (IWM-12)

Use the shared stylesheet, teal primary actions, readable dark text on a light
background, consistent spacing, cards and a constrained content width. Native
labels and controls remain associated. Provide a skip link, visible keyboard
focus, semantic headings and wrapping navigation. Controls target at least
44px height. At narrow widths cards stack; do not hide required fields.

## Requirements and test traceability

These FE identifiers describe this reduced scope, not full original SRS compliance.

| Requirement | Acceptance | Evidence |
| --- | --- | --- |
| FE-F01 | Delivered-page navigation targets exist | automated FE-01 |
| FE-F02 | All four application fields are labelled and required | FE-02; browser blank submit |
| FE-F03 | Reject malformed email, zero/negative/fractional amounts | FE-03, FE-04; browser invalid email/zero |
| FE-F04 | Valid demo form shows non-persistence feedback without navigation | FE-05; browser valid application |
| FE-F05 | Login validation does not claim authentication or echo credentials | FE-06 |
| FE-F06 | Editing clears stale feedback; form-free pages work | FE-07, FE-08 |
| FE-N01 | Dashboard and form fit a 390px viewport | Nov 2 browser checks and screenshots |
| FE-N02 | Application controls have keyboard order and focus | Nov 2 browser Tab check |
| FE-S01 | Use synthetic data; do not store credentials/application data | FE-05/06; source review |
| FE-S02 | User input is never rendered as HTML | fixed textContent feedback; source review |

## Executed results

On 3 November, Node 22.14.0 ran eight node:test/jsdom cases: **8 passed,
0 failed**. Vite production build passed and emitted all six HTML routes.
Raw reports: [unit and coverage](reports/sprint-1-unit-and-coverage.txt) and
[build](reports/sprint-1-build.txt). Coverage is 100% lines, branches and functions
for **js/demo-forms.js only**. This is not coverage of HTML, CSS, browser internals,
the original backend SRS or the entire application. jsdom is not a real browser.

Real Chrome checks on 2 November: dashboard links visible; empty application
submit blocked; malformed email and amount zero invalid; valid fictional values
showed the no-save notice without navigation; keyboard order name → insurance
type → email → amount; no horizontal overflow at 390×844; dashboard console
reported no errors. Screenshots are in [evidence/2026-11-02](evidence/2026-11-02).
These browser observations preceded the extraction of the same form handlers
into demo-forms.js. The extracted handlers are covered by the Nov 3 automated tests.

## Remaining manual checks and closeout gates

Repeat the delivered-page click-through on the final PR build, including login,
keyboard focus and narrow layouts. Obtain an independent teammate review and
green remote CI before merge. IWM-7/8/9 require each teammate's actual local setup
confirmation; Anuj's machine cannot establish that evidence. Record any carryover
openly. Do not mark implementation Done or close the sprint before these outcomes
are resolved. The GitHub Project and one-minute Sprint 1 walkthrough are assessment
deliverables; their presence must be verified separately.
