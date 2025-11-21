import time
import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from tests.utils.auth_helpers import login

def find_chromium_binary():
    """Busca el ejecutable de Chromium en ubicaciones comunes de Windows"""
    possible_paths = [
        r"C:\Program Files\Chromium\Application\chrome.exe",
        r"C:\Program Files (x86)\Chromium\Application\chrome.exe",
        r"C:\Users\{}\AppData\Local\Chromium\Application\chrome.exe".format(os.getenv('USERNAME', '')),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    for base_path in [r"C:\Program Files", r"C:\Program Files (x86)"]:
        if os.path.exists(base_path):
            for root, dirs, files in os.walk(base_path):
                if "chrome.exe" in files and "Chromium" in root:
                    return os.path.join(root, "chrome.exe")
    return None

@pytest.fixture
def driver():
    """Fixture para crear y configurar el WebDriver"""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    chromium_path = find_chromium_binary()
    if chromium_path:
        options.binary_location = chromium_path
        print("✓ Usando Chromium")
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2,
    }
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    try:
        driver_path = ChromeDriverManager().install()
        if not driver_path.endswith('.exe'):
            driver_dir = os.path.dirname(driver_path)
            chromedriver_exe = os.path.join(driver_dir, "chromedriver.exe")
            if os.path.exists(chromedriver_exe):
                driver_path = chromedriver_exe
            else:
                parent_dir = os.path.dirname(driver_dir)
                for root, dirs, files in os.walk(parent_dir):
                    if "chromedriver.exe" in files:
                        potential_path = os.path.join(root, "chromedriver.exe")
                        if os.path.getsize(potential_path) > 1000:
                            driver_path = potential_path
                            break
        if os.path.exists(driver_path) and os.path.getsize(driver_path) > 1000:
            service = Service(driver_path)
            driver = webdriver.Chrome(service=service, options=options)
        else:
            driver = webdriver.Chrome(options=options)
    except Exception as e:
        print(f"⚠ Error al configurar chromedriver: {e}")
        driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_agregar_almacen(driver):
    """
    Prueba de aceptación: Verificar que se puede agregar un almacén llenando el formulario
    """
    login_url = "http://localhost:8080"
    login_result = login(driver, "AnaMartinez", "1234", login_url)
    assert login_result['token'] is not None, f"El login no fue exitoso. URL actual: {login_result['current_url']}"
    print("✓ Login exitoso")
    time.sleep(2)

    wait = WebDriverWait(driver, 15)

    # 1. Abrir sidebar
    try:
        sidebar_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/button'))
        )
        sidebar_button.click()
        print("✓ Sidebar abierto")
        time.sleep(1)
    except Exception as e:
        raise AssertionError(f"No se pudo abrir el sidebar: {e}")

    # 2. Ingresar a Almacenes
    try:
        almacenes_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/div[1]/ul/li[4]/a'))
        )
        almacenes_link.click()
        print("✓ Ingresó a la sección de Almacenes")
        time.sleep(2)
    except Exception as e:
        raise AssertionError(f"No se pudo ingresar a la sección de almacenes: {e}")

    # 3. Pulsar botón de agregar almacén
    try:
        add_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div[1]/button'))
        )
        add_button.click()
        print("✓ Botón de agregar almacén presionado")
        time.sleep(1)
    except Exception as e:
        raise AssertionError(f"No se pudo presionar el botón de agregar almacén: {e}")

    # 4. Llenar el formulario y presionar guardar
    try:
        ubicacion_input = wait.until(EC.presence_of_element_located((By.ID, "UBICACION")))
        fecha_input = wait.until(EC.presence_of_element_located((By.ID, "FECHA_ACTUALIZACION")))
        encargado_select = wait.until(EC.presence_of_element_located((By.ID, "ENCARGADO_ALMACEN_ID")))

        ubicacion_input.clear()
        ubicacion_input.send_keys("Almacén Central Selenium")
        fecha_input.clear()
        fecha_input.send_keys("2024-12-01")
        # Selecciona el primer encargado disponible
        options = encargado_select.find_elements(By.TAG_NAME, "option")
        if options:
            encargado_select.click()
            options[0].click()
        print("✓ Formulario de almacén llenado")

        guardar_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Guardar')]")
        ))
        guardar_button.click()
        print("✓ Botón Guardar presionado")
        time.sleep(2)  # Espera para que el modal se cierre automáticamente

        # Cerrar el modal (presionar el botón de cerrar)
        try:
            close_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-close-STORES"))
            )
            close_button.click()
            print("✓ Modal cerrado")
        except Exception as e:
            print(f"⚠ No se pudo cerrar el modal manualmente: {e}")

        time.sleep(3)  # Espera adicional antes de terminar la prueba

    except Exception as e:
        raise AssertionError(f"No se pudo llenar o enviar el formulario de almacén: {e}")

    # 5. Scroll hacia la tabla (opcional, si quieres visualizar la tabla)
    try:
        stores_table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table-STORES")))
        driver.execute_script("arguments[0].scrollIntoView(false);", stores_table)
        print("✓ Scroll hacia la tabla de almacenes realizado")
        time.sleep(3)  # Delay adicional al final para visualizar la tabla antes de terminar la prueba
    except Exception as e:
        print(f"⚠ No se pudo hacer scroll a la tabla: {e}")
        time.sleep(3)

    print("\n✅ Proceso de agregar almacén completado (sin validación de aparición en la lista)")