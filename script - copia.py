from sys import maxsize
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
import time
import pytest
import re

# ------------------------
# Datos de usuarios
# ------------------------
users_list = [
    ["mirimanti@gmail.com", "miri234554"],
    ["lailacos@gmail.com", "pasavigjjord21"],
    ["mimama@gmail.com", "nat88e3113321"]
]

PRICES = {
    "Combo Meal": 59,
    "Kids Meal": 39,
    "Burger": 45,
    "Vegan": 45,
    "Sides": 12
}


# Fixture Selenium
@pytest.fixture()
def setup():
    driver = webdriver.Chrome()
    driver.get("https://svburger1.co.il/#/HomePage")
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

# Helpers

def extract_amount(text):
    match = re.search(r"\d+(\.\d+)?", text)
    if match:
        return float(match.group())
    raise ValueError(f"No se pudo extraer número de: {text}")

def get_total_after(driver):
    total_label = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[contains(text(),"Total:")]'))
    )
    return extract_amount(total_label.text)

def click_reserve(driver):
    reserve_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Reserve")]'))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", reserve_button)
    try:
        reserve_button.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", reserve_button)

def click_send(driver):
    send_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Send")]'))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", send_button)
    send_button.click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//h3[contains(text(), "successfully received")]'))
    )

def calculate_total_expected(subtotal, service_sum=None):
    if service_sum is None:
        service_sum = round(subtotal * 0.1, 2)
    return round(subtotal + service_sum, 2)

def select_meal(driver, meal_name, quantity=1):
    meal_card = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f'//div[@class="card-body"][.//h5[text()="{meal_name}"]]'))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", meal_card)
    try:
        meal_card.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", meal_card)

    subtotal = PRICES[meal_name] * quantity
    return subtotal, quantity

def select_three_meals(driver, meals_with_qty):
    if len(meals_with_qty) > 4:
        raise ValueError("Only up to 3 different meals are allowed")
    subtotal_total = 0
    for meal_name, qty in meals_with_qty.items():
        sub, _ = select_meal(driver, meal_name, quantity=qty)
        subtotal_total += sub
    return subtotal_total


def update_meal_quantity(driver, meal_name, quantity):
    input_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, f'//div[label[contains(text(),"{meal_name}")]]/input')
        )
    )
    input_field.click()
    input_field.clear()
    input_field.send_keys(str(quantity))
    time.sleep(1)
    actual_value = input_field.get_attribute("value")

    if str(quantity).isdigit():
        if actual_value == str(quantity):
            print(f"{meal_name} quantity correctly updated to {actual_value}")
        else:
            raise AssertionError(f"{meal_name} quantity mismatch! Expected {quantity}, got {actual_value}")
    else:
        if actual_value in ["", "1"]:
            print(f"{meal_name} invalid input correctly defaulted to {actual_value}")
        else:
            raise AssertionError(f"{meal_name} accepted invalid input! Input was '{quantity}', actual value: '{actual_value}'")



def click_signup_and_wait_combo(driver, expect_alert=False):
    driver.find_element(By.XPATH, "//form//button[text()='Sign Up']").click()
    try:
        alert = WebDriverWait(driver, 2).until(EC.alert_is_present())
        if expect_alert:
            return alert
        else:
            print("Alert:", alert.text)
            alert.accept()
            raise AssertionError(f"Test failed: unexpected alert {alert.text}")
    except TimeoutException:
        pass

    combo = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//h5[text()="Combo Meal"]'))
    )
    return combo


# Sanity
def test_sanity_combo_only(setup):
    driver = setup
    test_login_set_1(driver, "mirimanti@gmail.com", "miri234554")
    subtotal, _ = select_meal(driver, "Combo Meal", quantity=1)
    click_reserve(driver)
    total_expected = calculate_total_expected(subtotal)
    click_send(driver)
    total_after = get_total_after(driver)
    assert total_after == total_expected


# Suite 1 - Sign In
@pytest.mark.parametrize("email,password", [
    ("mirimanti@gmail.com", "miri234554"),
    ("manticof.miri@yahoo.com", "@Miriam99"),
])
def test_login_set_1(setup, email, password):
    driver = setup
    driver.find_element(By.XPATH, "//a[@href='#/SignIn']/button").click()
    driver.find_element(By.XPATH, '//input[@placeholder ="Enter your email"]').send_keys(email)
    driver.find_element(By.XPATH, '//input[@placeholder ="Enter your password"]').send_keys(password)
    driver.find_element(By.XPATH, '//button[@type ="submit"]').click()
    combo_meal = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//h5[contains(text(), "Combo")]'))
    )
    assert combo_meal.is_displayed(), f"Login with {email} failed"

@pytest.mark.parametrize("email,password,expected_msg", [
    ("", "testing123##", "failed to log in"),
    ("mirimanti@gmail.com", "isra123!!", "failed to log in"),
])
def test_login_negative_cases_set1(setup, email, password, expected_msg):
    driver = setup
    driver.find_element(By.XPATH, "//a[@href='#/SignIn']/button").click()
    if email:
        driver.find_element(By.XPATH, '//input[@placeholder ="Enter your email"]').send_keys(email)
    if password:
        driver.find_element(By.XPATH, '//input[@placeholder ="Enter your password"]').send_keys(password)
    driver.find_element(By.XPATH, '//button[@type ="submit"]').click()
    WebDriverWait(driver, 5).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    assert expected_msg in alert.text.lower()
    print(f"{email} failed")
    print("Alert:", alert.text)
    alert.accept()


# Suite 2 Sign Up
def test_signup_required_fields_only(setup):
    driver = setup
    driver.find_element(By.XPATH, "//button[text()='Sign Up']").click()
    driver.find_element(By.XPATH, "//form/input[3]").send_keys("miri.am@gmail.com")
    driver.find_element(By.XPATH, "//form/input[4]").send_keys("@Test012")
    driver.find_element(By.XPATH, "//form/input[5]").send_keys("@Test012")
    combo = click_signup_and_wait_combo(driver)
    assert combo.is_displayed()

def test_signup_firstname_7_chars(setup):
    driver = setup
    driver.find_element(By.XPATH, "//button[text()='Sign Up']").click()
    driver.find_element(By.XPATH, "//form/input[1]").send_keys("Analiza")
    driver.find_element(By.XPATH, "//form/input[3]").send_keys("miri.am2@gmail.com")
    driver.find_element(By.XPATH, "//form/input[4]").send_keys("@Test012")
    driver.find_element(By.XPATH, "//form/input[5]").send_keys("@Test012")
    combo = click_signup_and_wait_combo(driver)
    assert combo.is_displayed()

def test_signup_lastname_6_chars(setup):
    driver = setup
    driver.find_element(By.XPATH, "//button[text()='Sign Up']").click()
    driver.find_element(By.XPATH, "//form/input[2]").send_keys("Cohenn")
    driver.find_element(By.XPATH, "//form/input[3]").send_keys("miri.am1@gmail.com")
    driver.find_element(By.XPATH, "//form/input[4]").send_keys("@Test012")
    driver.find_element(By.XPATH, "//form/input[5]").send_keys("@Test012")
    combo = click_signup_and_wait_combo(driver)
    assert combo.is_displayed()

def test_signup_password_10_chars(setup):
    driver = setup
    driver.find_element(By.XPATH, "//button[text()='Sign Up']").click()
    driver.find_element(By.XPATH, "//form/input[3]").send_keys("miri.am3@gmail.com")
    driver.find_element(By.XPATH, "//form/input[4]").send_keys("Abcdef12.3")
    driver.find_element(By.XPATH, "//form/input[5]").send_keys("Abcdef12.3")
    combo = click_signup_and_wait_combo(driver)
    assert combo.is_displayed()

def test_signup_all_fields_complete(setup):
    driver = setup
    driver.find_element(By.XPATH, "//button[text()='Sign Up']").click()
    driver.find_element(By.XPATH, "//form/input[1]").send_keys("Analiza")
    driver.find_element(By.XPATH, "//form/input[2]").send_keys("Cohenn")
    driver.find_element(By.XPATH, "//form/input[3]").send_keys("miri.am123@gmail.com")
    driver.find_element(By.XPATH, "//form/input[4]").send_keys("@Test012")
    driver.find_element(By.XPATH, "//form/input[5]").send_keys("@Test012")
    combo = click_signup_and_wait_combo(driver)
    assert combo.is_displayed()

def test_signup_firstname_in_hebrew(setup):
    driver = setup
    driver.find_element(By.XPATH, "//button[text()='Sign Up']").click()
    driver.find_element(By.XPATH, "//form/input[1]").send_keys("שלוםמיר")
    driver.find_element(By.XPATH, "//form/input[2]").send_keys("Cohenn")
    driver.find_element(By.XPATH, "//form/input[3]").send_keys("Manticof.miri@gmail.com")
    driver.find_element(By.XPATH, "//form/input[4]").send_keys("Miriam99@")
    driver.find_element(By.XPATH, "//form/input[5]").send_keys("Miriam99@")
    combo = click_signup_and_wait_combo(driver)
    try:
        alert_msg = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'alert') or contains(@class,'error') or self::p]"))
        )
        msg_text = alert_msg.text.strip()
        print("Alert:", msg_text)
        assert msg_text == "First name must be in English letters only", f"Unexpected alert: {msg_text}"

    except TimeoutException:
        assert False, "Non message"

    except TimeoutException:
        combo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h5[text()="Combo Meal"]'))
        )
        assert combo.is_displayed()


# Suite 3 Order + Confirmation

def test_combo_plus_kids_3_1(setup):
    driver = setup
    test_login_set_1(driver, "mirimanti@gmail.com", "miri234554")
    meals_qty = {"Combo Meal": 1, "Kids Meal": 1}
    subtotal = select_three_meals(driver, meals_qty)
    click_reserve(driver)
    total_expected = calculate_total_expected(subtotal)
    click_send(driver)
    total_after = get_total_after(driver)
    assert total_after == total_expected

def test_burger_plus_vegan_plus_sides_3_2(setup):
    driver = setup
    test_login_set_1(driver, "mirimanti@gmail.com", "miri234554")
    meals_qty = {"Burger": 1, "Vegan": 1, "Sides": 1}
    subtotal = select_three_meals(driver, meals_qty)
    click_reserve(driver)
    total_expected = calculate_total_expected(subtotal)
    click_send(driver)
    total_after = get_total_after(driver)
    assert total_after == total_expected

def test_logout_functionality_3_3(setup):
    driver = setup
    test_login_set_1(driver, "mirimanti@gmail.com", "miri234554")
    try:
        menu_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@id="user-menu"]'))
        )
        menu_button.click()
    except:
        pass
    logout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((
            By.XPATH,
            '//a[contains(text(), "Log out")] | //button[contains(text(), "Log out")]'
        ))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", logout_button)
    driver.execute_script("arguments[0].click();", logout_button)
    welcome_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "Welcome to")]'))
    )
    time.sleep(2)
    assert welcome_message.is_displayed()

def test_update_combo_quantity_3_4(setup):
    driver = setup
    test_login_set_1(driver, "mirimanti@gmail.com", "miri234554")
    meals_qty = {"Combo Meal": 1}
    subtotal = select_three_meals(driver, meals_qty)
    click_reserve(driver)
    update_meal_quantity(driver, "Combo Meal", 2)
    click_send(driver)
    total_after = get_total_after(driver)
    total_expected = calculate_total_expected(PRICES["Combo Meal"] * 2)
    time.sleep(4)
    assert total_after == total_expected


def test_insert_table_number_3_5(setup):
    driver = setup
    test_login_set_1(driver, "mirimanti@gmail.com", "miri234554")
    meals_qty = {"Kids Meal": 1, }
    subtotal = select_three_meals(driver, meals_qty)
    click_reserve(driver)
    total_expected = calculate_total_expected(subtotal)
    table_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[label[normalize-space(.)="table No."]]/input'))
    )
    table_input.clear()
    table_input.send_keys("2")
    assert table_input.get_attribute("value") == "2"
    click_send(driver)
    final_table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//h3[contains(normalize-space(.), "2")]')
        )
    )
    assert "2" in final_table.text, f"Didnt find it 'Table No. 2', real text: {final_table.text}"
    print("Correct Table Number")
    total_after = get_total_after(driver)
    assert total_after == total_expected

from selenium.common.exceptions import TimeoutException

def test_update_combo_quantity_invalid_value_3_6(setup):
    driver = setup
    test_login_set_1(driver, "mirimanti@gmail.com", "miri234554")

    meals_qty = {"Combo Meal": 1}
    subtotal = select_three_meals(driver, meals_qty)
    click_reserve(driver)

    update_meal_quantity(driver, "Combo Meal", 3)
    click_send(driver)

    try:
        error_message = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[contains(text(), "Invalid value in quantity")]')
            )
        )
        print(f"✅ Found error message: {error_message.text}")
        assert "Invalid value in quantity" in error_message.text
    except TimeoutException:
        print("Error message not found.")
        assert False, "Expected error message was not displayed"


def test_insert_table_invalid_character_3_7(setup):
    driver = setup
    test_login_set_1(driver, "mirimanti@gmail.com", "miri234554")
    meals_qty = {"Combo Meal": 1,}
    subtotal = select_three_meals(driver, meals_qty)
    click_reserve(driver)
    total_expected = calculate_total_expected(subtotal)
    table_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[label[normalize-space(.)="table No."]]/input'))
    )
    table_input.clear()
    table_input.send_keys("a")
    value = table_input.get_attribute("value")
    time.sleep(2)
    assert value != "a", f"The input accepted an invalid character: {value}"
    assert value in ["", "1"], f"The unexpected value in the input was: {value}"
    print("Test passed: Table input rejected invalid character 'a'.")
