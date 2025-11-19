import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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


def test_login_page_aceptacion(driver):
    """
    Prueba de aceptación:
    Verificar que el login funciona correctamente con username AnaMartinez y password 1234
    """

    # ============= 1. PREPARACIÓN DE LA PRUEBA =============
    login_url = "http://localhost:8080"
    driver.get(login_url)

    # Espera a que la página cargue completamente
    time.sleep(3)

    # ============= 2. LÓGICA DE LA PRUEBA ==================
    # Buscar el campo de username por id="username"
    username_field = driver.find_element(By.ID, "username")
    
    # Buscar el campo de password por id="password"
    password_field = driver.find_element(By.ID, "password")
    
    # Buscar el botón de submit por type="submit"
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    # Ingresar credenciales
    username_field.clear()
    username_field.send_keys("AnaMartinez")
    
    password_field.clear()
    password_field.send_keys("1234")

    # Hacer clic en el botón de submit
    submit_button.click()

    # Esperar a que se procese el login (puede redirigir o mostrar mensaje)
    time.sleep(3)

    # ============= 3. VALIDACIÓN / ACEPTACIÓN ==============
    # Verificar que el login fue exitoso
    # Opción 1: Verificar que se redirigió al dashboard (URL cambió)
    current_url = driver.current_url
    print(f"URL actual después del login: {current_url}")
    
    # Verificar que el token se guardó en localStorage
    token = driver.execute_script("return localStorage.getItem('token');")
    print(f"Token guardado: {token is not None}")
    
    # Validaciones principales
    assert token is not None, "El token no se guardó en localStorage después del login"
    assert "dashboard" in current_url.lower() or token is not None, "El login no fue exitoso o no se redirigió correctamente"

