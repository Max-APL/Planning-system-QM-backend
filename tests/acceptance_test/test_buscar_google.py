import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    """
    1. Preparación general de la prueba (setup global):
       - Crear instancia de WebDriver (Chrome)
       - Entregarla al test
       - Cerrar el navegador al final
    """
    # Opcional: configurar opciones de Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    # Instalar y usar automáticamente el chromedriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    yield driver  # aquí se ejecuta el test

    # Teardown: cerrar navegador
    driver.quit()


def test_boton_buscar_con_google(driver):
    """
    Prueba de aceptación:
    Verificar que el botón de búsqueda tenga el texto "Buscar con Google"
    """

    # ============= 1. PREPARACIÓN DE LA PRUEBA =============
    google_url = "https://www.google.com"
    driver.get(google_url)

    # ============= 2. LÓGICA DE LA PRUEBA ==================
    # Espera simple para que cargue la página (igual que el sleep de Java)
    time.sleep(3)

    # Buscar el botón "Buscar con Google" por name="btnK"
    boton = driver.find_element(By.NAME, "btnK")

    # Obtener el texto del botón (atributo 'value', como en el código Java)
    txt_boton = boton.get_attribute("value")
    print("Texto del botón:", txt_boton)

    # ============= 3. VALIDACIÓN / ACEPTACIÓN ==============
    assert txt_boton == "Buscar con Google"
