import pytest
from pages.signup_page import SignupPage, generate_unique_email

# ── Bug reasons ───────────────────────────────────────────────────────────────
BUG_OPTIONAL_FIELDS = "BUG: First name and last name are optional per requirements, but the site rejects signup without them."
BUG_HEBREW_NAME     = "BUG: Hebrew first name should trigger a validation alert, but behaviour is inconsistent."


@pytest.mark.xfail(reason=BUG_OPTIONAL_FIELDS, strict=True)
def test_2_1_signup_required_fields_only(driver):
    page = SignupPage(driver)
    assert page.signup_succeeds(generate_unique_email(), "@Test012")

@pytest.mark.xfail(reason=BUG_OPTIONAL_FIELDS, strict=True)
def test_2_2_signup_firstname_7_chars(driver):
    page = SignupPage(driver)
    assert page.signup_succeeds(generate_unique_email(), "@Test012", firstname="Analiza")

@pytest.mark.xfail(reason=BUG_OPTIONAL_FIELDS, strict=True)
def test_2_3_signup_lastname_6_chars(driver):
    page = SignupPage(driver)
    assert page.signup_succeeds(generate_unique_email(), "@Test012", lastname="Cohenn")

@pytest.mark.xfail(reason=BUG_OPTIONAL_FIELDS, strict=True)
def test_2_4_signup_password_10_chars(driver):
    page = SignupPage(driver)
    assert page.signup_succeeds(generate_unique_email(), "Abcdef12.3")

def test_2_5_signup_all_fields(driver):
    page = SignupPage(driver)
    assert page.signup_succeeds(generate_unique_email(), "@Test012", firstname="Analiza", lastname="Cohenn")

@pytest.mark.xfail(reason=BUG_HEBREW_NAME, strict=False)
def test_2_6_signup_firstname_hebrew(driver):
    page = SignupPage(driver)
    alert_text = page.signup_expects_alert(
        generate_unique_email(), "Miriam99@",
        firstname="שלוםמיר",  # 7 chars in Hebrew
        lastname="Cohenn"
    )
    assert "english" in alert_text.lower() or "first name" in alert_text.lower(), \
        f"Unexpected alert message: {alert_text}"