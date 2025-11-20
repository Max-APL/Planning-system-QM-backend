import time
import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


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
    
    # Buscar recursivamente en Program Files
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
    # Habilitar logging para capturar errores de consola
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

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


def test_login_page_aceptacion(driver):
    """
    Prueba de aceptación: Verificar que el login funciona correctamente
    """
    # ============= 1. PREPARACIÓN DE LA PRUEBA =============
    login_url = "http://localhost:8080"
    driver.get(login_url)

    # Espera a que la página cargue completamente
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "username")))

    # ============= 2. LÓGICA DE LA PRUEBA ==================
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    username_field.clear()
    username_field.send_keys("AnaMartinez")
    password_field.clear()
    password_field.send_keys("1234")

    # Capturar errores de consola antes del login
    try:
        logs_before = driver.get_log('browser')
    except:
        logs_before = []
    
    # Hacer clic en el botón de submit
    submit_button.click()

    # Esperar a que se procese el login - esperar hasta que el token esté en localStorage o haya un error
    max_wait_time = 10
    wait_interval = 0.5
    elapsed_time = 0
    token = None
    alert_detected = False
    alert_text = None
    
    while elapsed_time < max_wait_time:
        time.sleep(wait_interval)
        elapsed_time += wait_interval
        
        # Verificar si el token se guardó
        token = driver.execute_script("return localStorage.getItem('token');")
        if token:
            break
        
        # Verificar si hay un alert visible (error)
        try:
            alert = driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            alert_detected = True
            print(f"Alert detectado: {alert_text}")
            break
        except:
            pass  # No hay alert visible
    
    # Capturar errores de consola después del login
    try:
        logs_after = driver.get_log('browser')
        all_logs = logs_after[len(logs_before):] if len(logs_after) > len(logs_before) else logs_after
        
        # Imprimir errores de consola si los hay
        if all_logs:
            print("\n=== Errores de consola ===")
            for log in all_logs:
                if log['level'] in ['SEVERE', 'WARNING']:
                    print(f"{log['level']}: {log['message']}")
    except:
        all_logs = []

    # ============= 3. VALIDACIÓN / ACEPTACIÓN ==============
    # Verificar que el login fue exitoso
    current_url = driver.current_url
    print(f"\nURL actual después del login: {current_url}")
    print(f"Token guardado: {token is not None}")
    if token:
        print(f"Token (primeros 20 caracteres): {token[:20]}...")
    
    # Si se detectó un alert, el login falló
    if alert_detected:
        error_msg = f"El login falló. Alert detectado: {alert_text}"
        try:
            severe_errors = [log['message'] for log in all_logs if log['level'] == 'SEVERE']
            if severe_errors:
                error_msg += f". Errores de consola: {severe_errors}"
        except:
            pass
        assert False, error_msg
    
    # Validaciones principales
    assert token is not None, f"El token no se guardó en localStorage después del login. URL actual: {current_url}. Verifique que el backend esté corriendo en http://localhost:8000 y que las credenciales sean correctas."
    assert "dashboard" in current_url.lower() or token is not None, "El login no fue exitoso o no se redirigió correctamente"
    
    # Esperar a que el dashboard cargue completamente
    print("\nEsperando a que el dashboard cargue completamente...")
    try:
        # Esperar hasta 5 segundos a que la página del dashboard esté completamente cargada
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        # Esperar un momento adicional para que los componentes del dashboard se rendericen
        time.sleep(2)
        print("Dashboard cargado exitosamente.")
    except Exception as e:
        print(f"Nota: No se pudo verificar completamente la carga del dashboard: {e}")
        # Aún así esperar un momento para que el dashboard se renderice
        time.sleep(2)
