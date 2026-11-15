# System validation - frontend release

Application baseline: eb232fb0ff13fb5d2fc197b8b5d8526e01c7723b (PR38 merge). Browser evidence captured 15 November on the identical PR head content before merge; no new post-merge browser session is claimed.

| Check | Actual observation | Evidence |
| --- | --- | --- |
| All six routes | Rendered; page headings inspected | index/login/dashboard/application/applications/staff PNGs |
| Keyboard staff action | Enter on first Approve changed selected card | staff-actions.png; recorded browser session |
| Independent staff action | Reject on second card left first approved | staff-actions.png |
| Refresh | Returned Under Review, Needs Information, Approved (Demo) fixtures | recorded browser reload; FE09 |
| Console | Captured error-level log list empty | recorded browser log query |
| Required fields/email/amount | Assertions passed | FE02-04, final-tests-coverage.txt |
| No-save form/login behavior | Assertions passed | FE05-07/10 |
| Build | Six output HTML pages produced | post-merge command and main-ci.json |

Historical manual report IWM35 predates final integration. Do not present it as an exhaustive regression of the final merge. Final full mobile matrix, screen-reader testing and production security/performance testing are not evidenced. No claim that all possible defects have been eliminated.

Known intentional limitations: no real authentication, persistence, upload, database, API or insurance decision; application list does not synchronize; View details disabled. These are documented scope limits, not hidden passing tests.
