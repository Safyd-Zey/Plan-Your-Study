import { test, expect } from '@playwright/test';

// Generate a unique value for every test run to avoid test data conflicts.
const makeUnique = (prefix: string) => `${prefix}-${Date.now()}-${Math.floor(Math.random() * 1000)}`;

test.describe('Plan Your Study web application', () => {
  test('registration and dashboard access works', async ({ page }) => {
    const uniqueId = makeUnique('playwright');
    const username = `user-${uniqueId}`;
    const email = `playwright+${uniqueId}@example.com`;
    const password = 'StrongPass123!';

    // Navigate to registration page and complete the signup flow.
    await page.goto('/register');
    await expect(page).toHaveURL(/.*\/register$/);

    await page.fill('#username', username);
    await page.fill('#email', email);
    await page.fill('#password', password);
    await page.fill('#confirmPassword', password);
    await page.click('button:has-text("Create Account")');

    await page.waitForURL(/.*\/dashboard$/);
    await expect(page.locator('text=Welcome back,')).toContainText(username);
    await expect(page.locator('text=Total Assignments')).toBeVisible();
  });

  test('course creation and assignment workflow is functional', async ({ page }) => {
    const uniqueId = makeUnique('playwright');
    const username = `user-${uniqueId}`;
    const email = `playwright+${uniqueId}@example.com`;
    const password = 'StrongPass123!';
    const courseName = `Automation Course ${uniqueId}`;
    const assignmentTitle = `Automation Assignment ${uniqueId}`;
    const deadline = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString().slice(0, 16);

    // Register a new user and verify dashboard access.
    await page.goto('/register');
    await page.fill('#username', username);
    await page.fill('#email', email);
    await page.fill('#password', password);
    await page.fill('#confirmPassword', password);
    await page.click('button:has-text("Create Account")');
    await page.waitForURL(/.*\/dashboard$/);

    await page.click('a:has-text("Courses")');
    await page.waitForURL(/.*\/courses$/);
    await page.click('button:has-text("New Course")');
    await page.fill('input[placeholder="e.g., Mathematics 101"]', courseName);
    await page.fill('textarea[placeholder="Course description"]', 'Course created by Playwright automation');
    await page.fill('input[placeholder="e.g., Dr. John Smith"]', 'Professor Automation');
    await page.click('button:has-text("Add Course")');
    await expect(page.locator(`text=${courseName}`)).toBeVisible();

    await page.click('a:has-text("Assignments")');
    await page.waitForURL(/.*\/assignments$/);
    await page.click('button:has-text("New Assignment")');
    await page.locator('select').first().selectOption({ label: courseName });
    await page.fill('input[placeholder="Assignment title"]', assignmentTitle);
    await page.fill('textarea[placeholder="Assignment description"]', 'Automated assignment created by Playwright');
    await page.fill('input[type="datetime-local"]', deadline);
    const prioritySelect = page.locator('select').nth(1);
    await prioritySelect.waitFor({ state: 'visible' });
    await prioritySelect.selectOption('high');
    await page.click('button:has-text("Create")');

    await expect(page.locator(`text=${assignmentTitle}`)).toBeVisible();
    await expect(page.locator('text=Upcoming')).toBeVisible();

    await page.click(`text=${assignmentTitle}`);
    await page.click('button:has-text("Start")');
    await expect(page.locator('button:has-text("Mark Completed")')).toBeVisible();
  });
});
