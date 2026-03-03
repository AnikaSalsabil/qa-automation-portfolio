# Test Plan - Sauce Labs Demo App
**Version:** 1.0  
**Author:** Anika Salsabil  
**Date:** March 04, 2026 
**Tool:** Selenium (Python), Playwright (JavaScript)

---

## 1. Project Overview

**Application Under Test (AUT):** Sauce Labs Demo App  
**URL:** https://www.saucedemo.com  
**Purpose:** Validate core e-commerce workflows — login, product browsing,
cart management, and checkout - to ensure functionality and reliability.

---

## 2. Scope

### In Scope
- User login (valid credentials, invalid credentials, locked account)
- Product catalogue page loading
- Add product to cart
- Remove product from cart
- Full checkout flow (fill form, confirm order)

### Out of Scope
- Payment gateway integration (no real payment processing)
- Backend/API testing
- Mobile responsive testing

---

## 3. Test Approach

A **risk-based approach** is used to prioritise testing.  
The login and checkout flows are the highest-risk user journeys - if
these fail, the entire application is unusable. These receive the most
test coverage.

**Test Levels Applied:**
- Functional testing (does each feature do what it should?)
- Negative testing (what happens with bad inputs?)
- Regression testing (do existing features break when we re-run?)
- UI validation (are elements visible and correct?)

---

## 4. Test Cases Summary

| ID    | Flow         | Test Description                   | Type        | Priority |
|-------|--------------|------------------------------------|-------------|----------|
| TC-01 | Login        | Valid login succeeds                | Functional  | High     |
| TC-02 | Login        | Invalid credentials shows error     | Negative    | High     |
| TC-03 | Login        | Locked-out user shows error         | Negative    | High     |
| TC-04 | Cart         | Add item increases cart badge       | Functional  | High     |
| TC-05 | Cart         | Remove item clears cart             | Functional  | Medium   |
| TC-06 | Checkout     | Full checkout completes             | Functional  | High     |
| TC-07 | Checkout     | Empty form shows validation error   | Negative    | Medium   |
| TC-08 | Products     | Product page loads after login      | Functional  | Medium   |

---

## 5. Entry Criteria
- Test environment (saucedemo.com) is accessible
- Test credentials are available (standard_user / secret_sauce)
- Automation scripts are written and reviewed
- Python and Node.js environments are configured

## 6. Exit Criteria
- All High priority test cases pass
- 0 Critical or High severity defects remain open
- HTML test reports generated for both Selenium and Playwright suites

---

## 7. Tools & Technologies

| Tool            | Purpose                          |
|-----------------|----------------------------------|
| Selenium        | Browser automation (Python)      |
| Playwright      | Browser automation (JavaScript)  |
| pytest          | Python test runner               |
| pytest-html     | HTML report generation           |
| GitHub Actions  | CI/CD pipeline                   |
| JIRA / GitHub Issues | Defect tracking             |

---

## 8. Risks & Mitigations

| Risk                              | Mitigation                          |
|-----------------------------------|-------------------------------------|
| Third-party site goes offline     | Tests will fail gracefully with clear error messages |
| Selector changes on saucedemo.com | Use stable IDs (data-test attributes) over CSS class names |
| Flaky tests from slow loading     | Add explicit waits instead of sleep() |

---

## 9. Test Environment

- **OS:** Windows 11 
- **Browser:** Chrome (headless in CI, headed locally)
- **Python:** 3.11+
- **Node.js:** 18+