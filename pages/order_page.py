import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from pages.base_page import BasePage


PRICES = {
    "Combo Meal": 59,
    "Kids Meal":  39,
    "Burger":     45,
    "Vegan":      45,
    "Sides":      12,
}


class OrderPage(BasePage):

    BTN_RESERVE   = (By.XPATH, '//button[contains(text(), "Reserve")]')
    BTN_SEND      = (By.XPATH, '//button[contains(text(), "Send")]')
    LABEL_TOTAL   = (By.XPATH, '//*[contains(text(),"Total:")]')
    MSG_SUCCESS   = (By.XPATH, '//h3[contains(text(), "successfully received")]')
    BTN_LOGOUT    = (By.XPATH, '//a[contains(text(), "Log out")] | //button[contains(text(), "Log out")]')
    WELCOME_MSG   = (By.XPATH, '//p[contains(text(), "Welcome to")]')

    # --- Helpers internos ---

    def _extract_amount(self, text):
        match = re.search(r"\d+(\.\d+)?", text)
        if match:
            return float(match.group())
        raise ValueError(f"No se pudo extraer número de: {text}")

    def calculate_expected_total(self, subtotal):
        service = round(subtotal * 0.1, 2)
        return round(subtotal + service, 2)

    def calculate_expected_subtotal_for_limit(self, meals_dict):
        """Returns the subtotal for the given meals dict using PRICES."""
        return sum(PRICES[meal] * qty for meal, qty in meals_dict.items())

    # --- Acciones de la página ---

    def select_meal(self, meal_name, quantity=1):
        card = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f'//div[@class="card-body"][.//h5[text()="{meal_name}"]]')
            )
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
        try:
            card.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", card)

        return PRICES[meal_name] * quantity

    def select_meals(self, meals_dict):
        if len(meals_dict) > 4:
            raise ValueError("Máximo 4 comidas distintas permitidas")
        total = 0
        for meal_name, qty in meals_dict.items():
            total += self.select_meal(meal_name, qty)
        return total

    def click_reserve(self):
        self.click(*self.BTN_RESERVE)

    def click_send(self):
        self.click(*self.BTN_SEND)
        self.wait.until(EC.visibility_of_element_located(self.MSG_SUCCESS))

    def get_displayed_total(self):
        label = self.wait.until(EC.visibility_of_element_located(self.LABEL_TOTAL))
        return self._extract_amount(label.text)

    def update_meal_quantity(self, meal_name, quantity):
        input_field = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f'//div[label[contains(text(),"{meal_name}")]]/input')
            )
        )
        input_field.click()
        input_field.clear()
        input_field.send_keys(str(quantity))
        time.sleep(1)
        actual = input_field.get_attribute("value")

        if str(quantity).isdigit():
            if actual != str(quantity):
                raise AssertionError(
                    f"{meal_name}: cantidad esperada {quantity}, obtenida {actual}"
                )
        else:
            if actual not in ["", "1"]:
                raise AssertionError(
                    f"{meal_name} aceptó valor inválido '{quantity}', valor real: '{actual}'"
                )

    def set_table_number(self, number):
        table_input = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[label[normalize-space(.)="table No."]]/input')
            )
        )
        table_input.clear()
        table_input.send_keys(str(number))
        return table_input.get_attribute("value")

    def get_confirmation_text(self):
        element = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//h3[contains(text(), "successfully received")]')
            )
        )
        return element.text

    def get_table_number_confirmation(self):
        element = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[contains(text(), "Table") or contains(text(), "table")]')
            )
        )
        return element.text

    def price_of(self, meal_name):
        return PRICES[meal_name]

    def logout(self):
        try:
            menu_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '//button[@id="user-menu"]'))
            )
            menu_btn.click()
        except Exception:
            pass
        self.click(*self.BTN_LOGOUT)
        return self.wait.until(EC.presence_of_element_located(self.WELCOME_MSG))

    def wait_for_invalid_quantity_message(self):
        return self.find(By.XPATH, "//*[contains(text(), 'Invalid value in quantity')]")

    def get_meal_element(self, meal_name):
        return self.find(
            By.XPATH,
            f'//div[@class="card-body"][.//h5[text()="{meal_name}"]]'
        )

    def is_meal_selection_disabled(self, meal_name):
        element = self.get_meal_element(meal_name)
        classes = element.get_attribute("class")
        is_disabled_attr = element.get_attribute("disabled")
        return is_disabled_attr is not None or "disabled" in classes or "not-clickable" in classes