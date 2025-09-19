const { test, expect } = require('@playwright/test');

test.describe('User Login', () => {
    const validUsername = 'tomsmith';
    const validPassword = 'SuperSecretPassword!';
    const invalidUsername = 'invalidUser';
    const invalidPassword = 'wrongPassword';

    test.beforeEach(async ({ page }) => {
        await page.goto('https://the-internet.herokuapp.com/login', { timeout: 10000 });
    });

    test('Positive Test: User can log in with valid credentials', async ({ page }) => {
        await page.fill('input#username', validUsername);
        await page.fill('input#password', validPassword);
        await page.click('button[type="submit"]');

        // Wait for navigation to secure page
        await page.waitForURL('https://the-internet.herokuapp.com/secure', { timeout: 10000 });

        // Assert that the user is redirected to the secure page
        const secureMessage = await page.locator('.flash.success').textContent();
        expect(secureMessage).toContain('You logged into a secure area!');
    });

    test('Negative Test: User cannot log in with invalid credentials', async ({ page }) => {
        await page.fill('input#username', invalidUsername);
        await page.fill('input#password', invalidPassword);
        await page.click('button[type="submit"]');

        // Wait for the error message to appear
        const errorMessage = await page.locator('.flash.error', { timeout: 10000 }).textContent();
        expect(errorMessage).toContain('Your username is invalid!');
    });
});