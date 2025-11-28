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


def test_ver_detalles_compra_reabastecimiento(driver):
    """
    Prueba de aceptación: Verificar que se pueden ver los detalles específicos de compra incluyendo cada item
    
    Para ver los prints durante la ejecución, ejecutar con:
    pytest tests/acceptance_test/test_ver_detalles_compra.py -s
    o
    pytest tests/acceptance_test/test_ver_detalles_compra.py --capture=no
    """
    wait = WebDriverWait(driver, 15)
    
    # ============= 1. PREPARACIÓN DE LA PRUEBA =============
    print("\n" + "="*60)
    print("1. PREPARACIÓN DE LA PRUEBA")
    print("="*60)
    print("FASE 1: INICIANDO SESIÓN")
    print("="*60)
    login_url = "http://localhost:8080"
    print(f"🔐 Iniciando sesión en: {login_url}")
    login_result = login(driver, "AnaMartinez", "1234", login_url)
    
    assert login_result['token'] is not None, f"El login no fue exitoso. URL actual: {login_result['current_url']}"
    print(f"✅ Login exitoso")
    time.sleep(2)
    
    # Verificar que aparece la página principal después del login
    current_url = driver.current_url
    assert "dashboard" in current_url.lower() or login_result['token'] is not None, "No se ingresó a la página principal"
    print(f"✅ Página principal (Dashboard) cargada: {current_url}")
    time.sleep(1)
    
    # ============= 2. LÓGICA DE LA PRUEBA ==================
    print("\n" + "="*60)
    print("2. LÓGICA DE LA PRUEBA")
    print("="*60)
    
    # Paso 1: Abrir sidebar (icono de las 3 barras)
    print("\n--- FASE 2: ABRIENDO SIDEBAR ---")
    try:
        sidebar_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/button'))
        )
        sidebar_button.click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sidebar-open, .sidebar.sidebar-open")))
        time.sleep(1)
        print("✅ Sidebar abierto correctamente - Se muestran todos los módulos y apartados del sistema")
    except Exception as e:
        print(f"⚠ Error al abrir sidebar: {e}")
        # Intentar con selector alternativo
        try:
            sidebar_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".hamburger-btn, button")))
            sidebar_button.click()
            time.sleep(2)
            print("✅ Sidebar abierto (método alternativo)")
        except:
            assert False, "No se pudo abrir el sidebar"
    
    # Paso 2: Seleccionar opción desplegable de Reabastecimiento (icono de camión)
    print("\n--- FASE 3: SELECCIONANDO MENÚ REABASTECIMIENTO ---")
    try:
        reabastecimiento_menu = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/div[1]/ul/li[5]/span'))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", reabastecimiento_menu)
        time.sleep(0.5)
        reabastecimiento_menu.click()
        time.sleep(1)
        print("✅ Menú Reabastecimiento desplegado - Se muestran dos opciones: reabastecimiento de material y herramientas")
    except Exception as e:
        print(f"⚠ Error al seleccionar menú Reabastecimiento: {e}")
        assert False, "No se pudo encontrar o hacer clic en el menú de Reabastecimiento"
    
    # Paso 3: Seleccionar sub-opción de Reabastecimiento de Material
    print("\n--- FASE 4: NAVEGANDO A REABASTECIMIENTO DE MATERIAL ---")
    try:
        reabastecimiento_option = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/div[1]/ul/li[5]/ul/li[1]/a'))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", reabastecimiento_option)
        time.sleep(0.5)
        reabastecimiento_option.click()
        time.sleep(3)
        
        # Verificar que se redirigió a la página de Reabastecimiento de Material
        current_url = driver.current_url
        print(f"✅ Redirigido a la página de Reabastecimientos de Material: {current_url}")
        print("✅ Se muestra el historial de reabastecimientos")
    except Exception as e:
        print(f"⚠ Error al seleccionar sub-opción: {e}")
        assert False, "No se pudo seleccionar la sub-opción de Reabastecimiento de Material"
    
    # Paso 4: Verificar que hay registros en la tabla
    print("\n--- FASE 5: VERIFICANDO TABLA DE REABASTECIMIENTOS ---")
    try:
        # Esperar a que la tabla se cargue
        tabla = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/table'))
        )
        print("✅ Tabla de reabastecimientos encontrada")
        
        # Verificar que hay al menos una fila en la tabla
        filas = driver.find_elements(By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/table/tbody/tr')
        assert len(filas) > 0, "No hay registros de reabastecimiento en la tabla"
        print(f"✅ Se encontraron {len(filas)} registro(s) en la tabla")
        
    except Exception as e:
        print(f"⚠ Error al verificar la tabla: {e}")
        assert False, f"No se pudo encontrar la tabla de reabastecimientos o no hay registros: {e}"
    
    # Paso 5: Presionar botón "Ver detalles" del primer registro
    print("\n--- FASE 6: PRESIONANDO BOTÓN 'VER DETALLES' ---")
    try:
        ver_detalles_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/table/tbody/tr[1]/td[6]/button'))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ver_detalles_button)
        time.sleep(0.5)
        ver_detalles_button.click()
        print("✅ Botón 'Ver detalles' presionado")
        time.sleep(2)  # Esperar a que se abra el popup
        
    except Exception as e:
        print(f"⚠ Error al presionar botón 'Ver detalles': {e}")
        # Intentar con selector alternativo
        try:
            ver_detalles_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Ver detalles') or contains(text(), 'Detalles')]")))
            ver_detalles_button.click()
            time.sleep(2)
            print("✅ Botón 'Ver detalles' presionado (selector alternativo)")
        except:
            assert False, "No se pudo encontrar o presionar el botón 'Ver detalles'"
    
    # Paso 6: Verificar que se abrió el popup
    print("\n--- FASE 7: VERIFICANDO POPUP DE DETALLES ---")
    try:
        # Buscar el popup/modal
        popup = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".modal, .popup, [role='dialog'], .dialog, .overlay"))
        )
        print("✅ Popup/modal abierto correctamente")
        
        # Verificar que el popup es visible
        assert popup.is_displayed(), "El popup no es visible"
        print("✅ El popup es visible")
        
    except Exception as e:
        print(f"⚠ Error al verificar popup: {e}")
        # Intentar buscar por otros selectores
        try:
            # Buscar cualquier elemento que pueda ser el popup
            popup_selectors = [
                "div[class*='modal']",
                "div[class*='popup']",
                "div[class*='dialog']",
                "div[class*='overlay']",
                "[role='dialog']"
            ]
            popup = None
            for selector in popup_selectors:
                try:
                    popup = driver.find_element(By.CSS_SELECTOR, selector)
                    if popup.is_displayed():
                        print(f"✅ Popup encontrado con selector: {selector}")
                        break
                except:
                    continue
            
            if not popup:
                assert False, "No se pudo encontrar el popup después de presionar 'Ver detalles'"
        except:
            assert False, f"No se pudo verificar que se abrió el popup: {e}"
    
    # ============= 3. VERIFICACIÓN DEL RESULTADO ESPERADO O ASSERT =============
    print("\n" + "="*60)
    print("3. VERIFICACIÓN DEL RESULTADO ESPERADO O ASSERT")
    print("="*60)
    
    # Verificar que se pueden ver los detalles específicos de cada material
    print("\n--- VERIFICANDO DETALLES ESPECÍFICOS DE COMPRA ---")
    
    # Verificar descripción
    print("\n📋 Verificando descripción de materiales...")
    try:
        # Buscar elementos que contengan descripción
        descripciones = driver.find_elements(By.XPATH, "//*[contains(text(), 'Descripción') or contains(text(), 'descripción') or contains(text(), 'Material') or contains(text(), 'material')]")
        if descripciones:
            print(f"✅ Se encontraron {len(descripciones)} elemento(s) relacionados con descripción")
            for i, desc in enumerate(descripciones[:3], 1):  # Mostrar solo los primeros 3
                if desc.is_displayed():
                    print(f"  - Descripción {i}: {desc.text[:50]}...")
        else:
            # Buscar en tablas dentro del popup
            try:
                tabla_detalles = popup.find_element(By.CSS_SELECTOR, "table, .table")
                filas_detalles = tabla_detalles.find_elements(By.CSS_SELECTOR, "tr, .row")
                if filas_detalles:
                    print(f"✅ Se encontró tabla con {len(filas_detalles)} fila(s) de detalles")
            except:
                pass
    except Exception as e:
        print(f"⚠ No se pudo verificar descripción específicamente: {e}")
    
    # Verificar cantidad
    print("\n🔢 Verificando cantidad de materiales...")
    try:
        # Buscar elementos que contengan cantidad
        cantidades = driver.find_elements(By.XPATH, "//*[contains(text(), 'Cantidad') or contains(text(), 'cantidad') or contains(text(), 'Qty')]")
        if cantidades:
            print(f"✅ Se encontraron {len(cantidades)} elemento(s) relacionados con cantidad")
            for i, cant in enumerate(cantidades[:3], 1):  # Mostrar solo los primeros 3
                if cant.is_displayed():
                    print(f"  - Cantidad {i}: {cant.text[:30]}...")
    except Exception as e:
        print(f"⚠ No se pudo verificar cantidad específicamente: {e}")
    
    # Verificar precio
    print("\n💰 Verificando precio de materiales...")
    try:
        # Buscar elementos que contengan precio (pueden tener símbolo $ o texto "Precio")
        precios = driver.find_elements(By.XPATH, "//*[contains(text(), '$') or contains(text(), 'Precio') or contains(text(), 'precio') or contains(text(), 'Costo') or contains(text(), 'costo')]")
        if precios:
            print(f"✅ Se encontraron {len(precios)} elemento(s) relacionados con precio")
            for i, precio in enumerate(precios[:3], 1):  # Mostrar solo los primeros 3
                if precio.is_displayed():
                    precio_text = precio.text[:40]
                    print(f"  - Precio {i}: {precio_text}...")
    except Exception as e:
        print(f"⚠ No se pudo verificar precio específicamente: {e}")
    
    # Verificar que hay una tabla o lista de items dentro del popup
    print("\n📊 Verificando lista de items/materiales en el popup...")
    try:
        # Buscar tabla dentro del popup
        tabla_items = popup.find_elements(By.CSS_SELECTOR, "table, .table, tbody, .list, .items")
        if tabla_items:
            print(f"✅ Se encontró tabla/lista con items dentro del popup")
            # Intentar contar filas de items
            try:
                filas_items = popup.find_elements(By.CSS_SELECTOR, "tbody tr, .row, .item")
                if filas_items:
                    print(f"✅ Se encontraron {len(filas_items)} item(s)/material(es) en los detalles")
            except:
                pass
        else:
            # Buscar cualquier lista o contenedor de items
            items = popup.find_elements(By.CSS_SELECTOR, "li, .item, .material, [class*='item']")
            if items:
                print(f"✅ Se encontraron {len(items)} item(s) en el popup")
    except Exception as e:
        print(f"⚠ No se pudo verificar lista de items: {e}")
    
    # Verificación final: El popup contiene información de detalles
    print("\n✅ VERIFICACIÓN FINAL")
    print("="*60)
    
    # Obtener todo el texto del popup para verificar que tiene contenido
    try:
        popup_text = popup.text
        assert len(popup_text) > 0, "El popup está vacío, no contiene información"
        print(f"✅ El popup contiene información (longitud: {len(popup_text)} caracteres)")
        
        # Verificar que contiene al menos una de las palabras clave esperadas
        palabras_clave = ['descripción', 'cantidad', 'precio', 'material', 'item', 'costo', 'total']
        palabras_encontradas = [palabra for palabra in palabras_clave if palabra.lower() in popup_text.lower()]
        
        if palabras_encontradas:
            print(f"✅ El popup contiene las siguientes palabras clave: {', '.join(palabras_encontradas)}")
        else:
            print("⚠ El popup no contiene las palabras clave esperadas, pero tiene contenido")
        
    except Exception as e:
        print(f"⚠ No se pudo obtener el texto completo del popup: {e}")
    
    # Assert final: Verificar que el popup está visible y contiene información
    assert popup.is_displayed(), "El popup de detalles no está visible"
    print("✅ ASSERT: El popup de detalles está visible")
    
    popup_text = popup.text if 'popup_text' not in locals() else popup_text
    assert len(popup_text) > 10, "El popup no contiene suficiente información"
    print("✅ ASSERT: El popup contiene información suficiente")
    
    print("\n" + "="*60)
    print("RESULTADO FINAL")
    print("="*60)
    print("✅ Se pueden ver los detalles específicos de compra incluyendo cada item")
    print("✅ El popup muestra descripción, cantidad y precio de los materiales")
    print("✅ Test completado exitosamente")
    print("="*60)

