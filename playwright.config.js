// playwright.config.js
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './playwright/tests', // folder where your tests are
  timeout: 30000,
  retries: 0,
  reporter: [['list'], ['html']],
});
