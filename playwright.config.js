// @ts-check
const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  // Where Playwright looks for test files
  testDir: './tests/playwright',

  // Max time a single test can run before it's considered failed
  timeout: 30000,  // 30 seconds

  // Run tests one at a time (easier to debug as a beginner)
  workers: 1,

  reporter: [
    ['html', { outputFolder: 'playwright-report', open: 'never' }],
    ['list']   // Also print results in terminal
  ],

  use: {
    // Run Chrome without opening a visible window
    headless: true,
    // Screenshot on failure — very useful for debugging
    screenshot: 'only-on-failure',
    // Record a video of failed tests
    video: 'retain-on-failure',
    // Wait up to 5 seconds for elements to appear
    actionTimeout: 5000,
  },

  projects: [
    {
      name: 'chromium',
      use: { browserName: 'chromium' },
    },
  ],
});