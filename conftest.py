import pytest
from selenium import webdriver


@pytest.fixture()
def driver():
    """
    Fixture compartido: abre Chrome, va al sitio, y lo cierra al terminar.
    Disponible para todos los tests automáticamente.
    """
    d = webdriver.Chrome()
    d.get("https://svburger1.co.il/#/HomePage")
    d.maximize_window()
    d.implicitly_wait(10)
    yield d
    d.quit()
