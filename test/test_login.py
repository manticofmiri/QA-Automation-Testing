import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.login_page import LoginPage


def test_1_1_login_yahoo(driver):
    page = LoginPage(driver)
    assert page.login_succeeds("manticof.miri@yahoo.com", "@Miriam99"), \
        "Login con Yahoo falló"
def test_1_2_login_gmail(driver):
    page = LoginPage(driver)
    assert page.login_succeeds("mirimanti@gmail.com", "miri234554"), \
        "Login con Gmail falló"
def test_1_3_login_without_email(driver):
    page = LoginPage(driver)
    alert_text = page.login_expects_alert("", "testing123##")
    print(f"\nAlert message: {alert_text}")
    assert "failed to log in" in alert_text.lower(), \
        f"Mensaje de error inesperado: {alert_text}"
def test_1_4_login_wrong_password(driver):
    page = LoginPage(driver)
    alert_text = page.login_expects_alert("mirimanti@gmail.com", "isra11123!!")
    print(f"\nAlert message: {alert_text}")
    assert "failed to log in" in alert_text.lower(), \
        f"Mensaje de error inesperado: {alert_text}"

