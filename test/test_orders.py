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


# ──────────────────────────────────────────
# Sanity
# ──────────────────────────────────────────

def test_sanity_combo_only(driver):
    order = login_and_go_to_order(driver)
    subtotal = order.select_meal("Combo Meal", quantity=1)
    order.click_reserve()
    expected = order.calculate_expected_total(subtotal)
    order.click_send()
    assert order.get_displayed_total() == expected


# ──────────────────────────────────────────
# Suite 3 – Order + Confirmation
# ──────────────────────────────────────────

def test_combo_plus_kids_3_1(driver):
    order = login_and_go_to_order(driver)
    subtotal = order.select_meals({"Combo Meal": 1, "Kids Meal": 1})
    order.click_reserve()
    expected = order.calculate_expected_total(subtotal)
    order.click_send()
    assert order.get_displayed_total() == expected


def test_burger_vegan_sides_3_2(driver):
    order = login_and_go_to_order(driver)
    subtotal = order.select_meals({"Burger": 1, "Vegan": 1, "Sides": 1})
    order.click_reserve()
    expected = order.calculate_expected_total(subtotal)
    order.click_send()
    assert order.get_displayed_total() == expected


def test_logout_functionality_3_3(driver):
    order = login_and_go_to_order(driver)
    welcome = order.logout()
    time.sleep(2)
    assert welcome.is_displayed()


def test_update_combo_quantity_3_4(driver):
    order = login_and_go_to_order(driver)
    order.select_meals({"Combo Meal": 1})
    order.click_reserve()
    order.update_meal_quantity("Combo Meal", 2)
    order.click_send()
    expected = order.calculate_expected_total(order.select_meal("Combo Meal", 2))
    time.sleep(4)
    assert order.get_displayed_total() == expected


def test_insert_table_number_3_5(driver):
    order = login_and_go_to_order(driver)
    subtotal = order.select_meals({"Kids Meal": 1})
    order.click_reserve()
    expected = order.calculate_expected_total(subtotal)

    value = order.set_table_number(2)
    assert value == "2"

    order.click_send()
    confirm_text = order.get_confirmation_table_text()
    assert "2" in confirm_text, f"No se encontró 'Table No. 2' en: {confirm_text}"
    assert order.get_displayed_total() == expected


def test_update_quantity_invalid_value_3_6(driver):
    order = login_and_go_to_order(driver)
    order.select_meals({"Combo Meal": 1})
    order.click_reserve()
    order.update_meal_quantity("Combo Meal", 3)
    order.click_send()

    try:
        error_msg = order.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[contains(text(), "Invalid value in quantity")]')
            )
        )
        assert "Invalid value in quantity" in error_msg.text
    except TimeoutException:
        assert False, "El mensaje de error de cantidad inválida no apareció"


def test_insert_table_invalid_character_3_7(driver):
    order = login_and_go_to_order(driver)
    order.select_meals({"Combo Meal": 1})
    order.click_reserve()

    value = order.set_table_number("a")
    time.sleep(2)
    assert value != "a", f"El campo aceptó un carácter inválido: {value}"
    assert value in ["", "1"], f"Valor inesperado en el campo de mesa: {value}"
