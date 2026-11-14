# IWM-35: Six-Page Manual Test Report

## Test information
- Date: 2026-11-15
- Contributor: Raghav
- Branch: feat/IWM-35-manual-test-checklist
- Base: main
- Scope: Frontend-only manual verification

## Pages tested

| Page | Mobile | Keyboard | Links | Assets | Result |
|---|---|---|---|---|---|
| index.html | Pass | Pass | Pass | Pass | Pass |
| login.html | Pass | Pass | Pass | Pass | Pass |
| dashboard.html | Pass | Pass | Pass | Pass | Pass |
| application.html | Pass | Pass | Pass | Pass | Pass |
| applications.html | Pass | Pass | Pass | Pass | Pass |
| staff.html | Pass | Pass | Pass | Pass | Pass |

## Manual testing
- Viewport: iPhone 16 (Chrome device emulation)
- Keyboard navigation: Tab navigation checked.
- Focus indicators: Checked.
- Responsive layout: Checked.
- Internal navigation: Checked.
- Missing assets: None observed.
- Browser console: No errors observed.
- Cross-page regressions: None observed.
- Defects: None observed.

## Automated validation
- Tests passed: 10/10
- Tests failed: 0
- Line coverage: 100%
- Branch coverage: 100%
- Function coverage: 100%
- Production build: Passed
- git diff --check: Passed

## Limitations
IWM-29 coordinated interactions were not included
in this main-based verification because their PR
was still awaiting review and integration.

## Conclusion
All six frontend pages passed the recorded manual
checks. Automated tests and production build passed.
No defects were observed.

## Next action
Submit the verification report for review and request
Anuj's review.
