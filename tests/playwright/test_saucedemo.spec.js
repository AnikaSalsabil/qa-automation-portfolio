// Import the test and expect tools from Playwright
const { test, expect } = require('@playwright/test');

// ============================================================
// CONSTANTS — reuse these so we don't repeat ourselves
// ============================================================
const BASE_URL = 'https://www.saucedemo.com';
const VALID_USER = 'standard_user';
const VALID_PASS = 'secret_sauce';

// ============================================================
// HELPER FUNCTION — login steps shared across tests
// page = the browser tab Playwright is controlling
// ============================================================
async function login(page) {
  await page.goto(BASE_URL);
  await page.fill('#user-name', VALID_USER);  // # means "find by id"
  await page.fill('#password', VALID_PASS);
  await page.click('#login-button');
  await expect(page).toHaveURL(/inventory/);  // Verify login worked
}

// ============================================================
// GROUP: Login Tests
// test.describe groups related tests together in the report
// ============================================================
test.describe('Login functionality', () => {

  // ----------------------------------------
  // TEST 1 — Valid login navigates to inventory
  // ----------------------------------------
  test('Valid login goes to products page', async ({ page }) => {
    await page.goto(BASE_URL);
    await page.fill('#user-name', VALID_USER);
    await page.fill('#password', VALID_PASS);
    await page.click('#login-button');

    // Check we landed on the inventory/products page
    await expect(page).toHaveURL(/inventory/);

    // Also verify the product list is actually visible
    await expect(page.locator('.inventory_list')).toBeVisible();
  });

  // ----------------------------------------
  // TEST 2 — Invalid login shows an error message
  // ----------------------------------------
  test('Invalid login shows error message', async ({ page }) => {
    await page.goto(BASE_URL);
    await page.fill('#user-name', 'bad_user');
    await page.fill('#password', 'bad_password');
    await page.click('#login-button');

    // The error container should appear
    await expect(page.locator('.error-message-container')).toBeVisible();

    // The error text should say something about username/password
    const errorText = await page.locator('.error-message-container').innerText();
    expect(errorText.toLowerCase()).toContain('username and password');
  });

});

// ============================================================
// GROUP: Cart Tests
// ============================================================
test.describe('Shopping cart functionality', () => {

  // ----------------------------------------
  // TEST 3 — Adding an item updates the cart badge
  // ----------------------------------------
  test('Add item to cart updates badge count', async ({ page }) => {
    await login(page);  // Use our helper function

    // Click the first "Add to cart" button (there are 6 products)
    await page.locator('.btn_inventory').first().click();

    // The cart badge (the red number on the cart icon) should show "1"
    await expect(page.locator('.shopping_cart_badge')).toHaveText('1');
  });

  // ----------------------------------------
  // TEST 4 — Removing an item empties the cart
  // ----------------------------------------
  test('Remove item from cart clears the cart', async ({ page }) => {
    await login(page);

    // Add an item first
    await page.locator('.btn_inventory').first().click();

    // Click the shopping cart icon to go to the cart page
    await page.click('.shopping_cart_link');

    // Click the Remove button
    await page.click('.cart_button');

    // The cart should have 0 items now
    await expect(page.locator('.cart_item')).toHaveCount(0);
  });

});

// ============================================================
// GROUP: Checkout Tests
// ============================================================
test.describe('Checkout flow', () => {

  // ----------------------------------------
  // TEST 5 — Full checkout flow from start to finish
  // This is the most important test — it covers the
  // entire critical user journey in one test
  // ----------------------------------------
  test('Complete checkout flow shows confirmation', async ({ page }) => {
    await login(page);

    // 1. Add a product to the cart
    await page.locator('.btn_inventory').first().click();

    // 2. Go to the cart
    await page.click('.shopping_cart_link');

    // 3. Click Checkout
    // data-test is a special attribute added specifically for testing
    await page.click('[data-test="checkout"]');

    // 4. Fill in the customer information form
    await page.fill('[data-test="firstName"]', 'Test');
    await page.fill('[data-test="lastName"]', 'User');
    await page.fill('[data-test="postalCode"]', '2000');

    // 5. Continue to order summary
    await page.click('[data-test="continue"]');

    // 6. Finish the order
    await page.click('[data-test="finish"]');

    // 7. Verify the success message appears
    await expect(page.locator('.complete-header')).toBeVisible();

    // 8. Check the actual text says "Thank you"
    await expect(page.locator('.complete-header')).toContainText('Thank you');
  });

});