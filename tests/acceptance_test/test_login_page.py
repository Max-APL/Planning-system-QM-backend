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
    # Configurar opciones de Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # Habilitar logging para capturar errores de consola
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

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
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "username")))

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

