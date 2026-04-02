import uuid
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage


def generate_unique_email():
    # Crea algo como: user_a1b2c3d4@gmail.com
    return f"user_{str(uuid.uuid4())[:8]}@gmail.com"


class SignupPage(BasePage):
    """
    Page Object dedicated to the Sign Up flow of SVBurger.
    """

    # --- Locators ---
    BTN_SIGNUP_NAV        = (By.XPATH, "//button[text()='Sign Up']")
    SIGNUP_INPUT_FIRSTNAME = (By.XPATH, "//form/input[1]")
    SIGNUP_INPUT_LASTNAME  = (By.XPATH, "//form/input[2]")
    SIGNUP_INPUT_EMAIL     = (By.XPATH, "//form/input[3]")
    SIGNUP_INPUT_PASSWORD  = (By.XPATH, "//form/input[4]")
    SIGNUP_INPUT_CONFIRM   = (By.XPATH, "//form/input[5]")
    BTN_SUBMIT_SIGNUP      = (By.XPATH, "//form//button[text()='Sign Up']")
    COMBO_MEAL_TITLE       = (By.XPATH, '//h5[contains(text(), "Combo")]')

    # ------------------------------------------------------------------ #
    #  Navigation                                                          #
    # ------------------------------------------------------------------ #
    def go_to_signup(self):
        self.click(*self.BTN_SIGNUP_NAV)

    # ------------------------------------------------------------------ #
    #  Core action                                                         #
    # ------------------------------------------------------------------ #
    def signup(self, email, password, firstname="", lastname=""):
        """Fill and submit the signup form."""
        self.go_to_signup()
        if firstname:
            self.type_text(*self.SIGNUP_INPUT_FIRSTNAME, firstname)
        if lastname:
            self.type_text(*self.SIGNUP_INPUT_LASTNAME, lastname)
        self.type_text(*self.SIGNUP_INPUT_EMAIL, email)
        self.type_text(*self.SIGNUP_INPUT_PASSWORD, password)
        self.type_text(*self.SIGNUP_INPUT_CONFIRM, password)
        self.click(*self.BTN_SUBMIT_SIGNUP)

    # ------------------------------------------------------------------ #
    #  Result helpers                                                      #
    # ------------------------------------------------------------------ #
    def signup_succeeds(self, email, password, firstname="", lastname=""):
        """
        Performs signup and returns True if the food menu appears.
        Raises AssertionError if an unexpected alert is shown.
        """
        self.signup(email, password, firstname, lastname)
        try:
            alert = self.wait.until(EC.alert_is_present())
            text = alert.text
            alert.accept()
            raise AssertionError(f"Signup failed with unexpected alert: {text}")
        except TimeoutException:
            pass
        return self.is_visible(*self.COMBO_MEAL_TITLE)

    def signup_expects_alert(self, email, password, firstname="", lastname=""):
        """
        Performs signup and returns the alert text.
        Raises AssertionError if no alert appears.
        """
        self.signup(email, password, firstname, lastname)
        try:
            alert = self.wait.until(EC.alert_is_present())
            text = alert.text
            alert.accept()
            return text
        except TimeoutException:
            raise AssertionError("Expected a validation alert but none appeared.")