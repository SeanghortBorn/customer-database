import { test, expect } from '@playwright/test';

test('register -> login -> landing', async ({ page }) => {
  const unique = Date.now();
  const email = `e2e+${unique}@example.com`;
  const password = 'pw';

  // go to register page and create account
  await page.goto('/register');
  await page.getByLabel('Name').fill('E2E User');
  await page.getByLabel('Email').fill(email);
  await page.getByLabel('Password').fill(password);
  await Promise.all([
    page.waitForURL('**/login'),
    page.getByRole('button', { name: /Create account/i }).click(),
  ]);

  // now sign in with the same credentials
  await page.goto('/login');
  await page.getByLabel('Email').fill(email);
  await page.getByLabel('Password').fill(password);
  await Promise.all([
    page.waitForURL('**/'),
    page.getByRole('button', { name: /Sign in/i }).click(),
  ]);

  // landing page should show basic UI elements
  await expect(page.locator('text=People')).toBeVisible();
  await expect(page.locator('text=Properties')).toBeVisible();
});
