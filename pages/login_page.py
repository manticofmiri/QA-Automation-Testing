from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Página de login y signup del sitio SVBurger.
    """

    # --- Locators ---
    BTN_SIGNIN_NAV     = (By.XPATH, "//a[@href='#/SignIn']/button")
    BTN_SIGNUP_NAV     = (By.XPATH, "//button[text()='Sign Up']")
    INPUT_EMAIL        = (By.XPATH, '//input[@placeholder ="Enter your email"]')
    INPUT_PASSWORD     = (By.XPATH, '//input[@placeholder ="Enter your password"]')
    BTN_SUBMIT_LOGIN   = (By.XPATH, '//button[@type ="submit"]')
    BTN_SUBMIT_SIGNUP  = (By.XPATH, "//form//button[text()='Sign Up']")
    COMBO_MEAL_TITLE   = (By.XPATH, '//h5[contains(text(), "Combo")]')

    SIGNUP_INPUT_FIRSTNAME = (By.XPATH, "//form/input[1]")
    SIGNUP_INPUT_LASTNAME  = (By.XPATH, "//form/input[2]")
    SIGNUP_INPUT_EMAIL     = (By.XPATH, "//form/input[3]")
    SIGNUP_INPUT_PASSWORD  = (By.XPATH, "//form/input[4]")
    SIGNUP_INPUT_CONFIRM   = (By.XPATH, "//form/input[5]")

    def go_to_signin(self):
        self.click(*self.BTN_SIGNIN_NAV)

    def login(self, email, password):
        self.go_to_signin()
        self.type_text(*self.INPUT_EMAIL, email)
        self.type_text(*self.INPUT_PASSWORD, password)
        self.click(*self.BTN_SUBMIT_LOGIN)

    def login_succeeds(self, email, password):
        """Hace login y devuelve True si aparece el menú de comidas."""
        self.login(email, password)
        return self.is_visible(*self.COMBO_MEAL_TITLE)

    def login_expects_alert(self, email, password):
        """Hace login y devuelve el texto del alert de error."""
        self.login(email, password)
        self.wait.until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        text = alert.text
        alert.accept()
        return text

    def go_to_signup(self):
        self.click(*self.BTN_SIGNUP_NAV)

    def signup(self, email, password, firstname="", lastname=""):
        self.go_to_signup()
        if firstname:
            self.type_text(*self.SIGNUP_INPUT_FIRSTNAME, firstname)
        if lastname:
            self.type_text(*self.SIGNUP_INPUT_LASTNAME, lastname)
        self.type_text(*self.SIGNUP_INPUT_EMAIL, email)
        self.type_text(*self.SIGNUP_INPUT_PASSWORD, password)
        self.type_text(*self.SIGNUP_INPUT_CONFIRM, password)
        self.click(*self.BTN_SUBMIT_SIGNUP)

    def signup_succeeds(self, email, password, firstname="", lastname=""):
        """Hace signup y devuelve True si aparece el menú de comidas."""
        self.signup(email, password, firstname, lastname)
        try:
            alert = self.wait.until(EC.alert_is_present())
            text = alert.text
            alert.accept()
            raise AssertionError(f"Signup falló con alert inesperado: {text}")
        except TimeoutException:
            pass
        return self.is_visible(*self.COMBO_MEAL_TITLE)
