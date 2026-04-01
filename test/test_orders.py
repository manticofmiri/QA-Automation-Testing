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


def test_3_1_combo_plus_kids(driver):
    order = login_and_go_to_order(driver)
    subtotal = order.select_meals({"Combo Meal": 1, "Kids Meal": 1})
    order.click_reserve()
    expected = order.calculate_expected_total(subtotal)
    order.click_send()
    assert order.get_displayed_total() == expected
def test_3_2_burger_vegan_sides(driver):
    order = login_and_go_to_order(driver)
    subtotal = order.select_meals({"Burger": 1, "Vegan": 1, "Sides": 1})
    order.click_reserve()
    expected = order.calculate_expected_total(subtotal)
    order.click_send()
    assert order.get_displayed_total() == expected
def test_3_3_logout(driver):
    order = login_and_go_to_order(driver)
    welcome = order.logout()
    time.sleep(2)
    assert welcome.is_displayed(), "El mensaje de bienvenida no apareció tras el logout"
def test_3_4_kids_meal_quantity_2(driver):
    order = login_and_go_to_order(driver)
    order.select_meals({"Kids Meal": 1})
    order.click_reserve()
    order.update_meal_quantity("Kids Meal", 2)
    order.click_send()
    expected = order.calculate_expected_total(order.price_of("Kids Meal") * 2)
    assert order.get_displayed_total() == expected
def test_3_5_table_number_2_kids_meal(driver):
    order = login_and_go_to_order(driver)
    subtotal = order.select_meals({"Kids Meal": 1})
    order.click_reserve()
    expected = order.calculate_expected_total(subtotal)

    value = order.set_table_number(2)
    assert value == "2", f"El campo de mesa no guardó '2', tiene: {value}"

    order.click_send()
    success_text = order.get_confirmation_text()
    assert "successfully received" in success_text.lower(), \
        f"No apareció el mensaje de confirmación: {success_text}"

    table_text = order.get_table_number_confirmation()
    assert "2" in table_text, f"No se encontró el número de mesa '2' en: {table_text}"
def test_3_6_burger_quantity_3(driver):
    order = login_and_go_to_order(driver)
    order.select_meals({"Burger": 1})
    order.click_reserve()
    order.update_meal_quantity("Burger", 3)
    order.click_send()
    expected = order.calculate_expected_total(order.price_of("Burger") * 3)
    assert order.get_displayed_total() == expected
def test_3_7_table_number_letters(driver):
    order = login_and_go_to_order(driver)
    order.select_meals({"Combo Meal": 1})
    order.click_reserve()

    value = order.set_table_number("a")
    time.sleep(2)
    assert value != "a", f"El campo aceptó una letra: '{value}'"
    assert value in ["", "1"], f"Valor inesperado en el campo de mesa: '{value}'"
def test_3_8_quantity_3_combo_error(driver):
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
        assert False, "No apareció el mensaje de error de cantidad inválida"
def test_3_9_select_4_meals(driver):
    order = login_and_go_to_order(driver)
    subtotal = order.select_meals({
        "Burger":     1,
        "Combo Meal": 1,
        "Vegan":      1,
        "Sides":      1,
    })
    order.click_reserve()
    expected = order.calculate_expected_total(subtotal)
    order.click_send()
    assert order.get_displayed_total() == expected