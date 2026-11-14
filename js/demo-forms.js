
// Demo forms never navigate, send, echo, or persist entered values.
export function attachDemoForms(root) {
  // Applicant and login form behaviour
  root.querySelectorAll('[data-demo-form]').forEach((form) => {
    form.addEventListener('submit', (event) => {
      event.preventDefault();

      form.querySelector('[data-result]').textContent =
        form.dataset.demoForm === 'login'
          ? 'Demo fields checked. No sign-in occurred. Use the dashboard link to continue.'
          : 'Demo fields checked. Nothing was sent or saved; no insurance application was created.';
    });

    form.addEventListener('input', () => {
      form.querySelector('[data-result]').textContent = '';
    });
  });

  // Staff review demonstration behaviour
  const cards = root.querySelectorAll('[data-demo-review]');
  let hasAttachedStaffActions = false;

  cards.forEach((card) => {
    const status = card.querySelector('[data-review-status]');
    const result = card.querySelector('[data-review-result]');

    if (!status || !result) return;

    ['approve', 'reject'].forEach((action) => {
      const button = card.querySelector(
        `[data-review-action="${action}"]`
      );

      if (!button || button.dataset.handlerAttached === 'true') return;

      button.addEventListener('click', () => {
        const newStatus =
          action === 'approve' ? 'Approved (Demo)' : 'Rejected (Demo)';

        // Update only the card whose button was clicked.
        status.textContent = newStatus;

        // Announce the change accessibly.
        result.textContent =
          `Application ${card.dataset.demoReview}: ${newStatus}. ` +
          'This is a demonstration only. Nothing was saved or sent.';
      });

      // Enable only after its click handler has been attached.
      button.dataset.handlerAttached = 'true';
      button.disabled = false;
      hasAttachedStaffActions = true;
    });
  });

  // Replace the old disabled-controls explanation when actions are ready.
  const reviewNote = root.querySelector('#review-note-text');

  if (hasAttachedStaffActions && reviewNote) {
    reviewNote.textContent =
      'Approve and Reject update only the selected sample application. ' +
      'Changes are announced accessibly but nothing is saved or sent. ' +
      'Refresh restores the original sample statuses. The applicant list ' +
      'does not change, and View details remains disabled.';
  }
}
