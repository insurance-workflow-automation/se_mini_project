# Staff screen outline — IWM-17

Prepared by Anuj on 2 November 2026 after taking over missing Day 4 work.
Original planned owner: Aswin. This is an outline, not an implemented staff UI.

- Display a list of synthetic submissions with reference, applicant name,
  insurance type, requested amount and demo status.
- Reuse labels from application.html: Applicant name, Insurance type,
  Contact email and Requested amount (INR).
- Future status labels: Pending review, Approved (demo), Rejected (demo).
- Day 7 controls: View details, Approve and Reject. Until Day 8 behavior is
  explicitly chosen, controls must be disabled or clearly illustrative.
- Any future decision updates browser-only demonstration state. No insurer
  receives data, no staff authorization exists, and no real decision occurs.
- Do not implement applicant storage, real credentials or a backend.

staff.html remains the empty scaffold for the planned Day 7 implementation.
