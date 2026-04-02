# 🍔 SV Burger - QA Automation Suite

[![Ejecucion de Tests Automatizados](https://github.com/manticofmiri/QA-Automation-Testing/actions/workflows/pruebas.yml/badge.svg)](https://github.com/manticofmiri/QA-Automation-Testing/actions/workflows/pruebas.yml)


## 📋 Project Overview
This project contains a professional automated testing suite for the **SV Burger** web application. It demonstrates the implementation of a robust automation framework focusing on functional, negative, and boundary testing.

### 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Framework:** Pytest
* **Tool:** Selenium WebDriver
* **Pattern:** Page Object Model (POM)
* **CI/CD:** GitHub Actions

---

## 🚀 Key Features implemented
* **Page Object Model (POM):** Separated page logic from test scripts for high maintainability.
* **Dynamic Data Generation:** Integrated `uuid` and `datetime` to generate unique user emails for every signup test run.
* **Continuous Integration:** Automated test execution on every `push` to the main branch using GitHub Actions.
* **Negative Testing:** Validated system boundaries, such as meal selection limits and field data types.

---

## 🧪 Test Suite Summary
The suite covers the following critical areas:
1. **User Authentication:** Login and Signup flows with unique data.
2. **Order Management:** Selecting meals, updating quantities, and calculating totals.
3. **Validation Logic:** Testing field constraints (e.g., non-numeric table numbers, quantity limits).

### Known Issues (Documented Bugs)
The project intentionally uses `@pytest.mark.xfail` to document existing bugs in the application:
* **BUG-003:** Missing validation when ordering more than 2 units of the same item.
* **BUG-004:** Table number field incorrectly accepts alphabetical characters.
* **BUG-005:** Business logic failure: System allows selecting more than 3 types of meals.

---

## 💻 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/tu-usuario/tu-repo.git](https://github.com/tu-usuario/tu-repo.git)
