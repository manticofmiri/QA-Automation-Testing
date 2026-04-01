import pytest
from pages.login_page import LoginPage


@pytest.mark.parametrize("email,password", [
    ("mirimanti@gmail.com", "miri234554"),
    ("manticof.miri@yahoo.com", "@Miriam99"),
])
def test_login_valid_credentials(driver, email, password):
    page = LoginPage(driver)
    assert page.login_succeeds(email, password), f"Login con {email} falló"


@pytest.mark.parametrize("email,password,expected_msg", [
    ("", "testing123##", "failed to log in"),
    ("mirimanti@gmail.com", "isra123!!", "failed to log in"),
])
def test_login_invalid_credentials(driver, email, password, expected_msg):
    page = LoginPage(driver)
    alert_text = page.login_expects_alert(email, password)
    assert expected_msg in alert_text.lower()

