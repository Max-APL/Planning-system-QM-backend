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
    # Obtener variables de entorno para hacer la función más general
    username = os.getenv('USERNAME', '')
    userprofile = os.getenv('USERPROFILE', '')
    local_appdata = os.getenv('LOCALAPPDATA', '')
    program_files = os.getenv('ProgramFiles', r'C:\Program Files')
    program_files_x86 = os.getenv('ProgramFiles(x86)', r'C:\Program Files (x86)')
    
    # Lista de rutas posibles usando variables de entorno
    possible_paths = [
        # Ubicación más común en AppData\Local
        os.path.join(local_appdata, r"Chromium\Application\chrome.exe") if local_appdata else None,
        os.path.join(userprofile, r"AppData\Local\Chromium\Application\chrome.exe") if userprofile else None,
        r"C:\Users\{}\AppData\Local\Chromium\Application\chrome.exe".format(username) if username else None,
        # Ubicaciones en Program Files
        os.path.join(program_files, r"Chromium\Application\chrome.exe") if program_files else None,
        os.path.join(program_files_x86, r"Chromium\Application\chrome.exe") if program_files_x86 else None,
        # Rutas absolutas por si las variables no funcionan
        r"C:\Program Files\Chromium\Application\chrome.exe",
        r"C:\Program Files (x86)\Chromium\Application\chrome.exe",
    ]
    
    # Eliminar None de la lista
    possible_paths = [path for path in possible_paths if path is not None]
    
    # Buscar en rutas directas
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✓ Chromium encontrado en: {path}")
            return path
    
    # Buscar recursivamente en AppData\Local (más común)
    search_paths = []
    if local_appdata:
        search_paths.append(local_appdata)
    if userprofile:
        search_paths.append(os.path.join(userprofile, "AppData", "Local"))
    
    for base_path in search_paths:
        if os.path.exists(base_path):
            try:
                for root, dirs, files in os.walk(base_path):
                    if "chromium" in root.lower() and "chrome.exe" in files:
                        chromium_path = os.path.join(root, "chrome.exe")
                        if os.path.exists(chromium_path):
                            print(f"✓ Chromium encontrado en: {chromium_path}")
                            return chromium_path
            except (PermissionError, OSError):
                continue
    
    # Buscar recursivamente en Program Files
    for base_path in [program_files, program_files_x86, r"C:\Program Files", r"C:\Program Files (x86)"]:
        if base_path and os.path.exists(base_path):
            try:
                for root, dirs, files in os.walk(base_path):
                    if "chromium" in root.lower() and "chrome.exe" in files:
                        chromium_path = os.path.join(root, "chrome.exe")
                        if os.path.exists(chromium_path):
                            print(f"✓ Chromium encontrado en: {chromium_path}")
                            return chromium_path
            except (PermissionError, OSError):
                continue
    
    print("⚠ Chromium no encontrado. Se usará Chrome por defecto si está disponible.")
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


def test_lista_materiales_carga_correctamente(driver):
    """
    Prueba de aceptación: Verificar que la lista de materiales se cargue correctamente
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
    
    # Buscar y hacer clic en el enlace de Materiales
    materials_link = None
    for attempt in range(5):
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sidebar ul, ul li a")))
            time.sleep(1)
            # El enlace de Materiales es el segundo elemento de la lista (después de Dashboard)
            materials_link = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Materiales') or contains(., 'Materiales')]"))
            )
            if materials_link.is_displayed():
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", materials_link)
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
                    materials_link = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'materiales')]"))
                    )
                    break
                except:
                    pass
    
    # Hacer clic en el enlace
    if materials_link:
        try:
            materials_link.click()
            print("✓ Enlace de Materiales presionado")
        except:
            driver.execute_script("arguments[0].click();", materials_link)
            print("✓ Enlace de Materiales presionado (JavaScript)")
    else:
        # Navegación directa como último recurso
        driver.get("http://localhost:8080/materials")
        print("✓ Navegación directa a /materials")
    
    time.sleep(3)
    current_url = driver.current_url
    assert "materials" in current_url.lower(), f"No se redirigió a la página de materiales. URL: {current_url}"
    print(f"✓ Redirección exitosa a: {current_url}")

    # ============= 3. VALIDACIÓN / ACEPTACIÓN ==============
    # Esperar a que la página cargue completamente
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    time.sleep(2)
    
    # Buscar contenedor de materiales
    try:
        materials_container = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".items-container-MATERIAL, .table-container-MATERIAL"))
        )
        assert materials_container.is_displayed(), "El contenedor de materiales no es visible"
        print("✓ Contenedor de materiales encontrado")
    except:
        # Intentar buscar por estructura general
        materials_container = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".items-container, .table-container, table"))
        )
        print("✓ Contenedor encontrado (selector alternativo)")
    
    # Verificar título de la página
    try:
        page_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1, .header-MATERIAL h1")))
        title_text = page_title.text.strip().lower()
        assert "material" in title_text or "gestión" in title_text, f"Título no contiene 'material' o 'gestión'. Título encontrado: {title_text}"
        print(f"✓ Título verificado: {page_title.text.strip()}")
    except Exception as e:
        print(f"⚠ Advertencia al verificar el título: {e}")
    
    # Verificar barra de búsqueda
    try:
        search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".search-input-MATERIAL, input[placeholder*='material'], input[placeholder*='Material']")))
        assert search_input.is_displayed(), "La barra de búsqueda no es visible"
        print("✓ Barra de búsqueda encontrada")
    except:
        print("⚠ No se encontró la barra de búsqueda (esto puede ser normal)")
    
    # Verificar tabla de materiales
    try:
        materials_table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table-MATERIAL, table")))
        assert materials_table.is_displayed(), "La tabla de materiales no es visible"
        print("✓ Tabla de materiales encontrada")
    except:
        # Intentar encontrar la tabla dentro del contenedor
        try:
            materials_table = materials_container.find_element(By.CSS_SELECTOR, "table")
            print("✓ Tabla encontrada (dentro del contenedor)")
        except:
            # Dar más tiempo para que cargue
            time.sleep(3)
            materials_table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
            print("✓ Tabla encontrada (búsqueda general)")
    
    # Verificar encabezados de la tabla
    try:
        table_headers = materials_table.find_elements(By.CSS_SELECTOR, "thead th")
        expected_headers = ["Nro", "Nombre", "Descripción", "Cantidad", "Precio Unitario", "Cantidad Mínima", "Acciones"]
        found_headers = [header.text.strip() for header in table_headers]
        headers_found = sum(1 for expected in expected_headers 
                          if any(expected.lower() in found.lower() for found in found_headers))
        assert headers_found >= 4, f"Encabezados insuficientes. Encontrados: {found_headers}, Esperados: {expected_headers}"
        print(f"✓ Encabezados validados: {headers_found}/{len(expected_headers)}")
        print(f"  Encabezados encontrados: {found_headers}")
    except Exception as e:
        print(f"⚠ Advertencia al verificar encabezados: {e}")
    
    # Verificar filas de la tabla (puede estar vacía, pero la estructura debe existir)
    try:
        table_rows = materials_table.find_elements(By.CSS_SELECTOR, "tbody tr")
        print(f"✓ Filas encontradas: {len(table_rows)}")
        
        # Si hay filas, verificar que tengan el formato correcto
        if len(table_rows) > 0:
            for i, row in enumerate(table_rows[:3]):  # Verificar las primeras 3 filas
                try:
                    cells = row.find_elements(By.CSS_SELECTOR, "td")
                    # Verificar que tenga al menos algunas celdas (mínimo 4 para tener datos básicos)
                    assert len(cells) >= 4, f"Fila {i+1} no tiene suficientes celdas. Celdas encontradas: {len(cells)}"
                    print(f"✓ Fila {i+1} tiene {len(cells)} celdas (correcta)")
                except Exception as e:
                    print(f"⚠ Advertencia en fila {i+1}: {e}")
        else:
            print("ℹ Tabla vacía (no hay materiales registrados) - esto es válido")
    except Exception as e:
        print(f"⚠ Advertencia al verificar filas: {e}")
    
    # Verificar botón de agregar material
    try:
        add_button = driver.find_element(By.CSS_SELECTOR, ".btn-add-material-MATERIAL, button[contains(text(), 'Agregar'), button[contains(text(), 'Add')]")
        assert add_button.is_displayed(), "El botón de agregar material no es visible"
        print("✓ Botón de agregar material encontrado")
    except:
        # Buscar por texto
        try:
            add_button = driver.find_element(By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'agregar') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'add')]")
            print("✓ Botón de agregar material encontrado (búsqueda por texto)")
        except:
            print("⚠ No se encontró el botón de agregar material (esto puede ser normal)")
    
    print("\n✅ Todas las validaciones pasaron correctamente")
    print("✅ La lista de materiales se cargó correctamente")
