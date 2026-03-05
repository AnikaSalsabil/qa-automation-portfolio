# QA Automation Portfolio

![QA Tests](https://github.com/AnikaSalsabil/qa-automation-portfolio/actions/workflows/ci.yml/badge.svg)

Automated test suite for [Sauce Labs Demo App](https://www.saucedemo.com) built to demonstrate hands-on experience with Selenium and Playwright — covering login, cart, and checkout flows across two frameworks with CI/CD integration.

---

## What's Inside

| | |
|---|---|
| **Selenium (Python)** | 7 test cases using pytest, WebDriverWait, and pytest-html reporting |
| **Playwright (JavaScript)** | 5 test cases with grouped describe blocks and built-in HTML reporting |
| **Test Plan** | Scope, risk assessment, test types, entry/exit criteria |
| **Bug Log** | Defects found during exploratory testing, logged with severity and steps |
| **CI/CD** | GitHub Actions runs both suites automatically on every push |

---

## Test Coverage

### Selenium — `tests/selenium/test_saucedemo.py`

| Test | Type |
|---|---|
| Valid login navigates to products page | Functional |
| Invalid credentials shows error message | Negative |
| Locked-out user shows specific error | Negative |
| Products page loads with 6 items | Functional |
| Add item increases cart badge to 1 | Functional |
| Remove item empties the cart | Functional |
| Full checkout flow completes with confirmation | End-to-End |

### Playwright — `tests/playwright/test_saucedemo.spec.js`

| Test | Type |
|---|---|
| Valid login goes to products page | Functional |
| Invalid login shows error message | Negative |
| Add item to cart updates badge count | Functional |
| Remove item from cart clears the cart | Functional |
| Complete checkout flow shows confirmation | End-to-End |

---

## Running Locally

**Selenium (Python)**
```bash
pip install -r requirements.txt
pytest tests/selenium/ -v --html=reports/selenium_report.html --self-contained-html
```

**Playwright (JavaScript)**
```bash
npm install
npx playwright install chromium
npx playwright test
npx playwright show-report
```

---

## Reports

- Selenium: `reports/selenium_report.html` — open in any browser
- Playwright: run `npx playwright show-report` — interactive report with screenshots on failure

---

## Docs

- [`docs/test_plan.md`](docs/test_plan.md) — scope, risk assessment, entry/exit criteria
- [`docs/bug_log.md`](docs/bug_log.md) — defects found during testing

---

## Stack

Python 3.11 · Selenium 4 · pytest · pytest-html · Node.js 18 · Playwright · GitHub Actions
