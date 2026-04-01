import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture()
def driver():
    # 1. Configuramos opciones para que funcione en GitHub (sin pantalla)
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    # 2. Instalamos el driver automáticamente
    service = Service(ChromeDriverManager().install())
    
    # 3. Iniciamos el navegador con las opciones
    d = webdriver.Chrome(service=service, options=chrome_options)
    
    d.get("https://svburger1.co.il/#/HomePage")
    d.implicitly_wait(10)
    
    yield d
    d.quit()
