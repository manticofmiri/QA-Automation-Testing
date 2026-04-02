import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture()
def driver():
    chrome_options = Options()

    # DETECCIÓN AUTOMÁTICA:
    # Si detecta que está en GitHub Actions (CI), activa el modo invisible.
    # Si estás en tu PC, abrirá el navegador normal para que puedas debuguear.
    if os.environ.get('GITHUB_ACTIONS'):
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

    # Configuraciones de estabilidad (útiles en ambos entornos)
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-notifications")

    # Instalación automática del Driver
    service = Service(ChromeDriverManager().install())

    # Inicio del navegador
    d = webdriver.Chrome(service=service, options=chrome_options)

    # Configuración de la sesión
    d.get("https://svburger1.co.il/#/HomePage")
    d.implicitly_wait(10)

    yield d

    # Cierre seguro
    d.quit()