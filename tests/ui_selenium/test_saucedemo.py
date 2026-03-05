# ============================================================
# IMPORTS — tools we need
# ============================================================
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from webdriver_manager.chrome import ChromeDriverManager

# ============================================================
# CONSTANTS — login details for the test site
# ============================================================
BASE_URL = "https://www.saucedemo.com"
VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"

# ============================================================
# FIXTURE — runs before and after EVERY test
# Opens Chrome → gives the test a "driver" → closes Chrome
# ============================================================
@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")          # Run without opening a visible window
    options.add_argument("--no-sandbox")         # Required for Linux/CI environments
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    d = webdriver.Chrome(
        #service=Service(ChromeDriverManager().install()),
        options=options
    )

    d.set_page_load_timeout(20)
    # yield means: "give the test the driver, then come back here when done"
    yield d
    d.quit()  # Always close Chrome after each test


# ============================================================
# HELPER FUNCTION — login steps used by multiple tests
# Avoids repeating the same 4 lines in every test
# ============================================================
def login(driver, username=VALID_USER, password=VALID_PASS):
    driver.get(BASE_URL)
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()


# ============================================================
# TEST 1 — Valid login should go to the products page
# ============================================================
def test_valid_login(driver):
    login(driver)  # Use our helper to log in
    # After login, the URL should contain "inventory"
    assert "inventory" in driver.current_url, \
        f"Expected inventory page, got: {driver.current_url}"


# ============================================================
# TEST 2 — Invalid credentials should show an error message
# ============================================================
def test_invalid_login_shows_error(driver):
    login(driver, username="wrong_user", password="wrong_pass")
    # Find the error element and check it's visible
    error = driver.find_element(By.CLASS_NAME, "error-message-container")
    assert error.is_displayed(), "Error message should be visible for invalid login"


# ============================================================
# TEST 3 — Locked out user should see specific error text
# ============================================================
def test_locked_out_user(driver):
    login(driver, username="locked_out_user", password="secret_sauce")
    error = driver.find_element(By.CLASS_NAME, "error-message-container")
    assert "locked out" in error.text.lower(), \
        f"Expected 'locked out' message, got: {error.text}"


# ============================================================
# TEST 4 — Products page should load after login
# ============================================================
def test_products_page_loads(driver):
    login(driver)
    # Wait up to 5 seconds for the product list to appear
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
    )
    # Count the products — there should be 6
    products = driver.find_elements(By.CLASS_NAME, "inventory_item")
    assert len(products) == 6, f"Expected 6 products, found: {len(products)}"


# ============================================================
# TEST 5 — Adding an item increases the cart badge to 1
# ============================================================
def test_add_item_to_cart(driver):
    login(driver)
    # Click the first "Add to cart" button on the page
    driver.find_elements(By.CLASS_NAME, "btn_inventory")[0].click()
    # Check the cart badge now shows "1"
    cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert cart_badge.text == "1", f"Expected cart badge '1', got: {cart_badge.text}"


# ============================================================
# TEST 6 — Removing an item should clear the cart badge
# ============================================================
def test_remove_item_from_cart(driver):
    login(driver)
    # First add an item
    driver.find_elements(By.CLASS_NAME, "btn_inventory")[0].click()
    # Then go to the cart page
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    # Click Remove
    driver.find_element(By.CLASS_NAME, "cart_button").click()
    # The cart items list should now be empty
    cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(cart_items) == 0, "Cart should be empty after removing the item"


# ============================================================
# TEST 7 — Complete checkout flow end-to-end
# ============================================================
def test_checkout_completes_successfully(driver):
    login(driver)

    # Step 1: Add item to cart
    driver.find_elements(By.CLASS_NAME, "btn_inventory")[0].click()

    # Step 2: Go to cart
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    # Step 3: Click Checkout button
    driver.find_element(By.ID, "checkout").click()

    # Step 4: Fill in customer info form
    driver.find_element(By.ID, "first-name").send_keys("Test")
    driver.find_element(By.ID, "last-name").send_keys("User")
    driver.find_element(By.ID, "postal-code").send_keys("2000")

    # Step 5: Continue to order summary
    driver.find_element(By.ID, "continue").click()

    # Step 6: Confirm the order
    driver.find_element(By.ID, "finish").click()

    # Step 7: Check for the success confirmation header
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
    )
    confirmation = driver.find_element(By.CLASS_NAME, "complete-header")
    assert "thank you" in confirmation.text.lower(), \
        f"Expected thank you message, got: {confirmation.text}"