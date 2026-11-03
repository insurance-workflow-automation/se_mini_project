import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { JSDOM } from 'jsdom';
import { attachDemoForms } from '../js/demo-forms.js';

const page = (name) => new JSDOM(readFileSync(new URL('../' + name + '.html', import.meta.url), 'utf8'),
  { url: 'https://demo.example/' + name + '.html' });

test('FE-01: all internal links in delivered pages resolve to repository pages or anchors', () => {
  for (const name of ['index', 'login', 'dashboard', 'application']) {
    const dom = page(name);
    for (const a of dom.window.document.querySelectorAll('a[href]')) {
      const href = a.getAttribute('href');
      if (href.startsWith('#')) assert.ok(dom.window.document.getElementById(href.slice(1)), href);
      else assert.ok(existsSync(resolve(href)), href);
    }
    dom.window.close();
  }
});

test('FE-02: application fields are labelled and required', () => {
  const dom = page('application');
  const fields = [...dom.window.document.querySelectorAll('input,select')];
  assert.equal(fields.length, 4);
  for (const field of fields) {
    assert.ok(field.required);
    assert.ok(field.labels.length);
  }
  assert.equal(dom.window.document.querySelector('form').checkValidity(), false);
  dom.window.close();
});

test('FE-03: email validity rejects malformed input and accepts demo email', () => {
  const dom = page('application');
  const email = dom.window.document.getElementById('contact-email');
  email.value = 'invalid';
  assert.equal(email.validity.typeMismatch, true);
  email.value = 'demo@example.com';
  assert.equal(email.checkValidity(), true);
  dom.window.close();
});

test('FE-04: amount rejects zero, negative and fractional values', () => {
  const dom = page('application');
  const amount = dom.window.document.getElementById('requested-amount');
  for (const value of ['0', '-1', '1.5']) {
    amount.value = value;
    assert.equal(amount.checkValidity(), false, value);
  }
  amount.value = '1000';
  assert.equal(amount.checkValidity(), true);
  dom.window.close();
});

test('FE-05: valid application submit is cancelled with an honest non-persistence notice', () => {
  const dom = page('application');
  const doc = dom.window.document;
  attachDemoForms(doc);
  const values = { 'applicant-name': 'Demo Applicant', 'insurance-type': 'health',
    'contact-email': 'demo@example.com', 'requested-amount': '1000' };
  for (const [id, value] of Object.entries(values)) doc.getElementById(id).value = value;
  const form = doc.querySelector('form');
  assert.equal(form.checkValidity(), true);
  const event = new dom.window.Event('submit', { bubbles: true, cancelable: true });
  assert.equal(form.dispatchEvent(event), false);
  assert.ok(event.defaultPrevented);
  assert.match(doc.querySelector('[data-result]').textContent, /Nothing was sent or saved/);
  assert.equal(dom.window.localStorage.length, 0);
  assert.equal(dom.window.location.pathname, '/application.html');
  dom.window.close();
});

test('FE-06: login does not authenticate or echo entered credentials', () => {
  const dom = page('login');
  const doc = dom.window.document;
  attachDemoForms(doc);
  doc.getElementById('demo-username').value = 'example-user';
  doc.getElementById('demo-password').value = 'fictional-secret';
  const event = new dom.window.Event('submit', { cancelable: true });
  doc.querySelector('form').dispatchEvent(event);
  assert.ok(event.defaultPrevented);
  const message = doc.querySelector('[data-result]').textContent;
  assert.match(message, /No sign-in occurred/);
  assert.doesNotMatch(message, /fictional-secret|example-user/);
  assert.equal(dom.window.localStorage.length, 0);
  dom.window.close();
});

test('FE-07: editing a field clears stale feedback', () => {
  const dom = page('application');
  const doc = dom.window.document;
  attachDemoForms(doc);
  doc.querySelector('[data-result]').textContent = 'Previous result';
  doc.querySelector('input').dispatchEvent(new dom.window.Event('input', { bubbles: true }));
  assert.equal(doc.querySelector('[data-result]').textContent, '');
  dom.window.close();
});

test('FE-08: shared script tolerates pages without forms', () => {
  for (const name of ['index', 'dashboard', 'applications', 'staff']) {
    const dom = page(name);
    assert.doesNotThrow(() => attachDemoForms(dom.window.document));
    dom.window.close();
  }
});
