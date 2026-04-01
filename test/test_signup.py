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
    LoginPage(driver).login_succeeds(USER_EMAIL, USER_PASSWORD)
    return OrderPage(driver)

def test_2_1_signup_required_fields_only(driver):
    page = LoginPage(driver)
    assert page.signup_succeeds("miri.am@gmail.com", "@Test012")
def test_2_2_signup_firstname_7_chars(driver):
    page = LoginPage(driver)
    assert page.signup_succeeds(
        "miri.am2@gmail.com", "@Test012",
        firstname="Analiza"  # 7 chars
    )
def test_2_3_signup_lastname_6_chars(driver):
    page = LoginPage(driver)
    assert page.signup_succeeds(
        "miri.am1@gmail.com", "@Test012",
        lastname="Cohenn"  # 6 chars
    )
def test_2_4_signup_password_10_chars(driver):
    page = LoginPage(driver)
    assert page.signup_succeeds(
        "miri.am3@gmail.com", "Abcdef12.3"  # 10 chars
    )
def test_2_5_signup_all_fields(driver):
    page = LoginPage(driver)
    assert page.signup_succeeds(
        "miri.am888888@gmail.com", "@Test012",
        firstname="Analiza",
        lastname="Cohenn"
    )
def test_2_6_signup_firstname_hebrew(driver):
    page = LoginPage(driver)
    page.signup(
        "Manticof.miri@gmail.com", "Miriam99@",
        firstname="שלוםמיר",  # 7 chars in Hebrew
        lastname="Cohenn"
    )
    try:
        page.wait.until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert_text = alert.text
        print(f"\nAlert message: {alert_text}")
        alert.accept()
        assert "english" in alert_text.lower() or "first name" in alert_text.lower(), \
            f"Mensaje de alert inesperado: {alert_text}"
    except TimeoutException:
        assert False, "The alert with the validation message does not appear."



