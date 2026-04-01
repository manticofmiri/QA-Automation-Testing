import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.login_page import LoginPage
from pages.order_page import OrderPage

USER_EMAIL    = "mirimanti@gmail.com"
USER_PASSWORD = "miri234554"


def login_and_go_to_order(driver):
    """Helper: hace login y devuelve la instancia de OrderPage lista para usar."""
    LoginPage(driver).login_succeeds(USER_EMAIL, USER_PASSWORD)
    return OrderPage(driver)

def test_signup_required_fields_only(driver):
    page = LoginPage(driver)
    assert page.signup_succeeds("miri.am@gmail.com", "@Test012")


def test_signup_firstname_7_chars(driver):
    page = LoginPage(driver)
    assert page.signup_succeeds("miri.am2@gmail.com", "@Test012", firstname="Analiza")


def test_signup_lastname_6_chars(driver):
    page = LoginPage(driver)
    assert page.signup_succeeds("miri.am1@gmail.com", "@Test012", lastname="Cohenn")


def test_signup_password_10_chars(driver):
    page = LoginPage(driver)
    assert page.signup_succeeds("miri.am3@gmail.com", "Abcdef12.3")


def test_signup_all_fields_complete(driver):
    page = LoginPage(driver)
    assert page.signup_succeeds(
        "miri.am123456@gmail.com", "@Test012",
        firstname="Analiza", lastname="Cohenn"
    )


def test_signup_firstname_in_hebrew(driver):
    """
    Registrar con nombre en hebreo debería mostrar un mensaje de validación.
    """
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException

    page = LoginPage(driver)
    page.signup(
        "Manticof.miri@gmail.com", "Miriam99@",
        firstname="שלוםמיר", lastname="Cohenn"
    )

    try:
        alert_msg = page.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'alert') or contains(@class,'error') or self::p]")
            )
        )
        msg_text = alert_msg.text.strip()
        assert msg_text == "First name must be in English letters only", \
            f"Mensaje inesperado: {msg_text}"
    except TimeoutException:
        assert False, "No apareció el mensaje de validación para nombre en hebreo"
