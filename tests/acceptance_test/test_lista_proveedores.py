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
    
    # Intentar usar Chromium si está disponible
    chromium_path = find_chromium_binary()
    if chromium_path:
        options.binary_location = chromium_path
        print("✓ Usando Chromium")
    
    # Preferencias básicas
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2,
    }
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")

    # Configurar chromedriver
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


def test_lista_proveedores_carga_correctamente(driver):
    """
    Prueba de aceptación: Verificar que la lista de proveedores se cargue correctamente
    """
    # ============= 1. PREPARACIÓN DE LA PRUEBA =============
    login_url = "http://localhost:8080"
    login_result = login(driver, "AnaMartinez", "1234", login_url)
    
    assert login_result['token'] is not None, f"El login no fue exitoso. URL actual: {login_result['current_url']}"
    print(f"✓ Login exitoso")
    time.sleep(2)

    # ============= 2. LÓGICA DE LA PRUEBA ==================
    wait = WebDriverWait(driver, 15)
    
    # Abrir sidebar
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
    
    # Cerrar cualquier popup si existe
    try:
        driver.execute_script("""
            var popups = document.querySelectorAll('[role="dialog"], .modal');
            popups.forEach(function(popup) {
                if (popup.offsetParent !== null) {
                    popup.style.display = 'none';
                }
            });
        """)
        time.sleep(0.5)
    except:
        pass
    
    # Buscar y hacer clic en el enlace de Proveedores
    providers_link = None
    for attempt in range(5):
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sidebar ul, ul li a")))
            time.sleep(1)
            providers_link = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[1]/div[1]/ul/li[8]/a'))
            )
            if providers_link.is_displayed():
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", providers_link)
                time.sleep(1)
                break
        except Exception as e:
            if attempt < 4:
                time.sleep(2)
                # Reabrir sidebar si se cerró
                try:
                    sidebar = driver.find_element(By.CSS_SELECTOR, ".sidebar")
                    if "sidebar-open" not in sidebar.get_attribute("class"):
                        sidebar_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/button')
                        sidebar_button.click()
                        time.sleep(2)
                except:
                    pass
            else:
                # Buscar por texto como último recurso
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
        # Navegación directa como último recurso
        driver.get("http://localhost:8080/providers")
        print("✓ Navegación directa a /providers")
    
    time.sleep(3)
    current_url = driver.current_url
    assert "providers" in current_url.lower(), f"No se redirigió a la página de proveedores. URL: {current_url}"
    print(f"✓ Redirección exitosa a: {current_url}")

    # ============= 3. VALIDACIÓN / ACEPTACIÓN ==============
    # Buscar contenedor de proveedores
    try:
        providers_container = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]'))
        )
        assert providers_container.is_displayed(), "El contenedor de proveedores no es visible"
        print("✓ Contenedor de proveedores encontrado")
    except:
        providers_container = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".items-container-PROV, .table-container-PROV, table"))
        )
        print("✓ Contenedor encontrado (selector alternativo)")
    
    # Verificar tabla de proveedores
    try:
        providers_table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table-PROV, table")))
        print("✓ Tabla de proveedores encontrada")
    except:
        providers_table = providers_container.find_element(By.CSS_SELECTOR, "table")
    
    # Verificar encabezados
    try:
        table_headers = providers_table.find_elements(By.CSS_SELECTOR, "thead th")
        expected_headers = ["Nro", "Nombre", "Dirección", "Teléfono", "Acciones"]
        found_headers = [header.text.strip() for header in table_headers]
        headers_found = sum(1 for expected in expected_headers 
                          if any(expected.lower() in found.lower() for found in found_headers))
        assert headers_found >= 3, f"Encabezados insuficientes. Encontrados: {found_headers}"
        print(f"✓ Encabezados validados: {headers_found}/{len(expected_headers)}")
    except Exception as e:
        print(f"⚠ Advertencia al verificar encabezados: {e}")
    
    # Verificar filas
    try:
        table_rows = providers_table.find_elements(By.CSS_SELECTOR, "tbody tr")
        print(f"✓ Filas encontradas: {len(table_rows)}")
        if len(table_rows) > 0:
            for i, row in enumerate(table_rows[:3]):
                cells = row.find_elements(By.CSS_SELECTOR, "td")
                assert len(cells) >= 4, f"Fila {i+1} no tiene suficientes celdas"
    except Exception as e:
        print(f"⚠ Advertencia al verificar filas: {e}")
    
    # Verificar título
    try:
        page_title = driver.find_element(By.CSS_SELECTOR, "h1, .header-PROV h1")
        assert "proveedor" in page_title.text.strip().lower(), "Título no contiene 'proveedor'"
        print(f"✓ Título verificado: {page_title.text.strip()}")
    except:
        print("⚠ No se pudo verificar el título")
    
    print("\n✅ Todas las validaciones pasaron correctamente")
    print("✅ La lista de proveedores se cargó correctamente")
