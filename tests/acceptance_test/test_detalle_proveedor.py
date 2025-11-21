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

def test_detalle_proveedor(driver):
    """
    Prueba de aceptación: Verificar que se puede ver el detalle de un proveedor
    """
    # ============= 1. PREPARACIÓN DE LA PRUEBA =============
    login_url = "http://localhost:8080"
    login_result = login(driver, "AnaMartinez", "1234", login_url)
    assert login_result['token'] is not None, f"El login no fue exitoso. URL actual: {login_result['current_url']}"
    print(f"✓ Login exitoso")
    time.sleep(2)

    wait = WebDriverWait(driver, 15)

    # Abrir sidebar y navegar a Proveedores
    try:
        sidebar_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/button'))
        )
        sidebar_button.click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sidebar-open, .sidebar.sidebar-open")))
        time.sleep(2)
        print("✓ Sidebar abierto")
    except Exception as e:
        print(f"⚠ Error al abrir sidebar: {e}")
        sidebar_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".hamburger-btn, button")))
        sidebar_button.click()
        time.sleep(2)

    # Buscar y hacer clic en el enlace de Proveedores
    providers_link = None
    for attempt in range(5):
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sidebar ul, ul li a")))
            time.sleep(1)
            providers_link = wait.until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Proveedores')]"))
            )
            if providers_link.is_displayed():
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", providers_link)
                time.sleep(1)
                break
        except Exception as e:
            if attempt < 4:
                time.sleep(2)
                try:
                    sidebar = driver.find_element(By.CSS_SELECTOR, ".sidebar")
                    if "sidebar-open" not in sidebar.get_attribute("class"):
                        sidebar_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/button')
                        sidebar_button.click()
                        time.sleep(2)
                except:
                    pass
            else:
                try:
                    providers_link = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Proveedores')]"))
                    )
                    break
                except:
                    pass

    # Hacer clic en el enlace
    if providers_link:
        try:
            providers_link.click()
            print("✓ Enlace de Proveedores presionado")
        except:
            driver.execute_script("arguments[0].click();", providers_link)
            print("✓ Enlace de Proveedores presionado (JavaScript)")
    else:
        driver.get("http://localhost:8080/providers")
        print("✓ Navegación directa a /providers")

    time.sleep(3)
    current_url = driver.current_url
    assert "providers" in current_url.lower(), f"No se redirigió a la página de proveedores. URL: {current_url}"
    print(f"✓ Redirección exitosa a: {current_url}")

    # ============= 2. DETALLE DE PROVEEDOR ==================
    # Buscar la tabla de proveedores y hacer clic en el botón de detalle del primer proveedor
    try:
        providers_table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table-PROV, table")))
        print("✓ Tabla de proveedores encontrada")
        first_row = providers_table.find_element(By.CSS_SELECTOR, "tbody tr")
        # Busca el botón de detalle (puede ser un botón con texto "Ver", "Detalle" o un icono)
        detail_button = None
        try:
            detail_button = first_row.find_element(By.XPATH, ".//button[contains(text(), 'Detalle') or contains(text(), 'Ver')]")
        except:
            # Busca por clase o icono alternativo
            buttons = first_row.find_elements(By.TAG_NAME, "button")
            if buttons:
                detail_button = buttons[0]
        assert detail_button is not None, "No se encontró el botón de detalle en la primera fila"
        detail_button.click()
        print("✓ Botón de detalle presionado")
    except Exception as e:
        raise AssertionError(f"No se pudo acceder al detalle del proveedor: {e}")

    # ============= 3. VALIDACIÓN DEL DETALLE ================
    # Esperar a que se muestre el detalle (puede ser un modal o una nueva página)
    try:
        # Espera por el modal de detalle del proveedor
        detail_section = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal-PROV"))
        )
        assert detail_section.is_displayed(), "El detalle del proveedor no es visible"
        print("✓ Detalle del proveedor visible")

        # Validar que se muestre información relevante
        detail_text = detail_section.text.lower()
        assert "nombre" in detail_text and "dirección" in detail_text, "No se muestra información relevante del proveedor"
        print("✓ Información relevante del proveedor mostrada")
        time.sleep(2)  # Delay para visualizar el modal antes de cerrar la prueba
    except Exception as e:
        raise AssertionError(f"No se pudo validar el detalle del proveedor: {e}")

    print("\n✅ Todas las validaciones pasaron correctamente")
    print("✅ Se puede ver el detalle de un proveedor")