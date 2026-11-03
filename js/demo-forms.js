// Demo forms never navigate, send, echo, or persist entered values.
export function attachDemoForms(root) {
  root.querySelectorAll('[data-demo-form]').forEach((form) => {
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      form.querySelector('[data-result]').textContent = form.dataset.demoForm === 'login'
        ? 'Demo fields checked. No sign-in occurred. Use the dashboard link below to continue.'
        : 'Demo fields checked. Nothing was sent or saved; no insurance application was created.';
    });
    form.addEventListener('input', () => {
      form.querySelector('[data-result]').textContent = '';
    });
  });
}
