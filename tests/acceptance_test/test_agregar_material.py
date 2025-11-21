import time
import os
import random
import string
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


def test_agregar_material(driver):
    """
    Prueba de aceptación: Verificar que se puede agregar un nuevo material correctamente
    """
    # Generar nombre único para el material usando timestamp y caracteres aleatorios
    timestamp = str(int(time.time()))
    random_suffix = ''.join(random.choices(string.ascii_uppercase, k=4))
    material_name = f"Material Test {timestamp} {random_suffix}"
    
    # ============= 1. PREPARACIÓN DE LA PRUEBA =============
    login_url = "http://localhost:8080"
    login_result = login(driver, "AnaMartinez", "1234", login_url)
    
    assert login_result['token'] is not None, f"El login no fue exitoso. URL actual: {login_result['current_url']}"
    print(f"✓ Login exitoso")
    time.sleep(2)

    # ============= 2. NAVEGAR A LA PÁGINA DE MATERIALES ==================
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
    
    # Buscar y hacer clic en el enlace de Materiales
    materials_link = None
    for attempt in range(5):
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sidebar ul, ul li a")))
            time.sleep(1)
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
                try:
                    sidebar = driver.find_element(By.CSS_SELECTOR, ".sidebar")
                    if "sidebar-open" not in sidebar.get_attribute("class"):
                        sidebar_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/button')
                        sidebar_button.click()
                        time.sleep(2)
                except:
                    pass
    
    if materials_link:
        try:
            materials_link.click()
            print("✓ Enlace de Materiales presionado")
        except:
            driver.execute_script("arguments[0].click();", materials_link)
            print("✓ Enlace de Materiales presionado (JavaScript)")
    else:
        driver.get("http://localhost:8080/materials")
        print("✓ Navegación directa a /materials")
    
    time.sleep(3)
    current_url = driver.current_url
    assert "materials" in current_url.lower(), f"No se redirigió a la página de materiales. URL: {current_url}"
    print(f"✓ Redirección exitosa a: {current_url}")
    
    # Esperar a que la página cargue
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    time.sleep(2)
    
    # Obtener el número de filas antes de agregar el material
    try:
        materials_table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table-MATERIAL, table")))
        rows_before = len(materials_table.find_elements(By.CSS_SELECTOR, "tbody tr"))
        print(f"✓ Filas antes de agregar: {rows_before}")
    except:
        rows_before = 0
        print("⚠ No se pudo contar las filas antes de agregar")

    # ============= 3. ABRIR EL MODAL DE AGREGAR MATERIAL ==================
    # Buscar el botón de agregar material
    add_button = None
    try:
        add_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-add-material-MATERIAL"))
        )
        print("✓ Botón de agregar material encontrado")
    except:
        # Buscar por texto
        try:
            add_button = driver.find_element(By.XPATH, 
                "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'agregar') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'add')]")
            print("✓ Botón de agregar material encontrado (búsqueda por texto)")
        except:
            # Buscar cualquier botón que contenga el texto
            add_button = driver.find_element(By.XPATH, 
                "//button[contains(., '+') or contains(., 'Agregar') or contains(., 'Add')]")
            print("✓ Botón de agregar material encontrado (búsqueda alternativa)")
    
    # Hacer clic en el botón de agregar
    try:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_button)
        time.sleep(0.5)
        add_button.click()
        print("✓ Botón de agregar material presionado")
    except:
        driver.execute_script("arguments[0].click();", add_button)
        print("✓ Botón de agregar material presionado (JavaScript)")
    
    # Esperar a que el modal aparezca
    time.sleep(2)
    
    # Verificar que el modal se abrió
    try:
        modal = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-MATERIAL, .modal-overlay-MATERIAL .modal-MATERIAL")))
        assert modal.is_displayed(), "El modal de agregar material no es visible"
        print("✓ Modal de agregar material abierto")
    except:
        # Buscar modal de forma más general
        modal = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".modal, [role='dialog']")))
        print("✓ Modal encontrado (selector alternativo)")

    # ============= 4. LLENAR EL FORMULARIO ==================
    # Datos del material a agregar
    material_data = {
        "nombre": material_name,
        "descripcion": f"Descripción de prueba para {material_name}. Material de prueba automatizado.",
        "cantidad": "100",
        "precio": "25",
        "cantidadMinima": "10"
    }
    
    # Llenar campo Nombre
    try:
        nombre_field = wait.until(EC.presence_of_element_located((By.ID, "nombre")))
        nombre_field.clear()
        nombre_field.send_keys(material_data["nombre"])
        # Disparar eventos de Vue
        driver.execute_script("""
            var input = arguments[0];
            var value = arguments[1];
            input.value = value;
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
        """, nombre_field, material_data["nombre"])
        print(f"✓ Nombre ingresado: {material_data['nombre']}")
    except Exception as e:
        print(f"⚠ Error al ingresar nombre: {e}")
        raise
    
    time.sleep(0.5)
    
    # Llenar campo Descripción
    try:
        descripcion_field = wait.until(EC.presence_of_element_located((By.ID, "descripcion")))
        descripcion_field.clear()
        descripcion_field.send_keys(material_data["descripcion"])
        # Disparar eventos de Vue
        driver.execute_script("""
            var textarea = arguments[0];
            var value = arguments[1];
            textarea.value = value;
            textarea.dispatchEvent(new Event('input', { bubbles: true }));
            textarea.dispatchEvent(new Event('change', { bubbles: true }));
        """, descripcion_field, material_data["descripcion"])
        print(f"✓ Descripción ingresada")
    except Exception as e:
        print(f"⚠ Error al ingresar descripción: {e}")
        raise
    
    time.sleep(0.5)
    
    # Llenar campo Cantidad
    try:
        cantidad_field = wait.until(EC.presence_of_element_located((By.ID, "cantidad")))
        cantidad_field.clear()
        cantidad_field.send_keys(material_data["cantidad"])
        driver.execute_script("""
            var input = arguments[0];
            var value = arguments[1];
            input.value = value;
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
        """, cantidad_field, material_data["cantidad"])
        print(f"✓ Cantidad ingresada: {material_data['cantidad']}")
    except Exception as e:
        print(f"⚠ Error al ingresar cantidad: {e}")
        raise
    
    time.sleep(0.5)
    
    # Llenar campo Precio Unitario
    try:
        precio_field = wait.until(EC.presence_of_element_located((By.ID, "precio")))
        precio_field.clear()
        precio_field.send_keys(material_data["precio"])
        driver.execute_script("""
            var input = arguments[0];
            var value = arguments[1];
            input.value = value;
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
        """, precio_field, material_data["precio"])
        print(f"✓ Precio unitario ingresado: {material_data['precio']}")
    except Exception as e:
        print(f"⚠ Error al ingresar precio: {e}")
        raise
    
    time.sleep(0.5)
    
    # Llenar campo Cantidad Mínima
    try:
        cantidad_minima_field = wait.until(EC.presence_of_element_located((By.ID, "cantidadMinima")))
        cantidad_minima_field.clear()
        cantidad_minima_field.send_keys(material_data["cantidadMinima"])
        driver.execute_script("""
            var input = arguments[0];
            var value = arguments[1];
            input.value = value;
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
        """, cantidad_minima_field, material_data["cantidadMinima"])
        print(f"✓ Cantidad mínima ingresada: {material_data['cantidadMinima']}")
    except Exception as e:
        print(f"⚠ Error al ingresar cantidad mínima: {e}")
        raise
    
    time.sleep(1)
    
    # ============= 5. GUARDAR EL MATERIAL ==================
    # Buscar y hacer clic en el botón Guardar
    try:
        save_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-primary-MATERIAL, button[type='submit']"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_button)
        time.sleep(0.5)
        save_button.click()
        print("✓ Botón Guardar presionado")
    except:
        # Buscar por texto
        try:
            save_button = driver.find_element(By.XPATH, 
                "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'guardar') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'save')]")
            driver.execute_script("arguments[0].click();", save_button)
            print("✓ Botón Guardar presionado (búsqueda por texto)")
        except:
            # Último intento: buscar cualquier botón submit dentro del modal
            form = driver.find_element(By.CSS_SELECTOR, ".form-MATERIAL, form")
            save_button = form.find_element(By.CSS_SELECTOR, "button[type='submit']")
            driver.execute_script("arguments[0].click();", save_button)
            print("✓ Botón Guardar presionado (submit del form)")
    
    # Esperar a que se procese el guardado
    time.sleep(3)
    
    # Verificar que el modal se cerró
    try:
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal-MATERIAL")))
        print("✓ Modal cerrado (material guardado)")
    except:
        # Dar más tiempo
        time.sleep(2)
        try:
            modal = driver.find_element(By.CSS_SELECTOR, ".modal-MATERIAL")
            if not modal.is_displayed():
                print("✓ Modal cerrado")
            else:
                print("⚠ El modal aún está visible, pero continuamos")
        except:
            print("✓ Modal no encontrado (probablemente cerrado)")

    # ============= 6. SCROLL Y DELAY DESPUÉS DE GUARDAR ==================
    # Esperar un momento para que la página se actualice automáticamente
    time.sleep(2)
    
    # Hacer scroll hacia abajo para ver la tabla
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("✓ Scroll hacia abajo realizado")
        time.sleep(1)
    except:
        print("⚠ No se pudo hacer scroll")
    
    # Delay adicional antes de validar
    print("✓ Esperando a que la página se actualice...")
    time.sleep(3)

    # ============= 7. VALIDACIÓN / ACEPTACIÓN ==================
    # Buscar el material en la tabla (sin recargar, ya que se redirige automáticamente)
    material_found = False
    try:
        # Esperar a que la tabla esté disponible
        materials_table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table-MATERIAL, table")))
        table_rows = materials_table.find_elements(By.CSS_SELECTOR, "tbody tr")
        
        print(f"✓ Filas después de agregar: {len(table_rows)}")
        
        # Buscar el material por nombre en la tabla
        for row in table_rows:
            try:
                cells = row.find_elements(By.CSS_SELECTOR, "td")
                if len(cells) > 1:  # Asegurar que tiene al menos 2 celdas (Nro y Nombre)
                    cell_text = cells[1].text.strip()  # La segunda celda debería ser el nombre
                    if material_name in cell_text or material_data["nombre"] in cell_text:
                        material_found = True
                        print(f"✓ Material encontrado en la tabla: {cell_text}")
                        break
            except:
                continue
        
        if not material_found:
            # Intentar buscar en toda la tabla usando JavaScript
            material_in_table = driver.execute_script(f"""
                var table = document.querySelector('.table-MATERIAL, table');
                if (table) {{
                    return table.innerText.includes('{material_name}');
                }}
                return false;
            """)
            
            if material_in_table:
                material_found = True
                print(f"✓ Material encontrado en la tabla (búsqueda por JavaScript)")
        
    except Exception as e:
        print(f"⚠ Error al buscar el material en la tabla: {e}")
    
    # Delay final antes de terminar la prueba
    print("✓ Esperando un momento antes de finalizar...")
    time.sleep(2)
    
    # Validación final
    assert material_found, f"El material '{material_name}' no se encontró en la tabla después de agregarlo"
    
    print("\n✅ Todas las validaciones pasaron correctamente")
    print(f"✅ El material '{material_name}' se agregó correctamente")

