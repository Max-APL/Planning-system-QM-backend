"""
Utilidades para autenticación en tests de aceptación
"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login(driver, username: str, password: str, login_url: str = "http://localhost:8080", wait_time: int = 3):
    """
    Realiza el proceso de login en la aplicación.
    
    Args:
        driver: Instancia de WebDriver de Selenium
        username: Nombre de usuario para el login
        password: Contraseña para el login
        login_url: URL de la página de login (por defecto: http://localhost:8080)
        wait_time: Tiempo de espera en segundos después de cargar la página y después del submit (por defecto: 3)
    
    Returns:
        dict: Diccionario con información del login:
            - 'success': bool - Indica si el login fue exitoso
            - 'token': str - Token guardado en localStorage (None si no existe)
            - 'current_url': str - URL actual después del login
    """
    wait = WebDriverWait(driver, 10)
    
    # ============= 1. PREPARACIÓN =============
    driver.get(login_url)
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    time.sleep(wait_time)
    
    # ============= 2. LÓGICA ==================
    username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
    submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    
    # Actualizar valores en Vue
    driver.execute_script("""
        var username = arguments[0];
        var password = arguments[1];
        var app = document.querySelector('[data-v-app]') || document.querySelector('#app');
        if (app && app.__vue__) {
            var component = app.__vue__;
            while (component) {
                if (component.hasOwnProperty('username') || component.hasOwnProperty('password')) {
                    component.username = username;
                    component.password = password;
                    break;
                }
                component = component.$parent || component.$root;
            }
        }
    """, username, password)
    
    # Ingresar credenciales en los campos
    username_field.clear()
    username_field.send_keys(username)
    driver.execute_script("""
        var input = arguments[0];
        var value = arguments[1];
        input.value = value;
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
    """, username_field, username)
    
    time.sleep(0.3)
    
    password_field.clear()
    password_field.send_keys(password)
    driver.execute_script("""
        var input = arguments[0];
        var value = arguments[1];
        input.value = value;
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
    """, password_field, password)
    
    time.sleep(0.5)
    
    # Ejecutar login
    try:
        login_executed = driver.execute_script("""
            var app = document.querySelector('[data-v-app]') || document.querySelector('#app');
            if (app && app.__vue__) {
                var component = app.__vue__;
                while (component) {
                    if (component.login && typeof component.login === 'function') {
                        component.login();
                        return true;
                    }
                    component = component.$parent || component.$root;
                }
            }
            return false;
        """)
        
        if not login_executed:
            # Si no se ejecutó el método login(), hacer clic en el botón
            try:
                submit_button.click()
            except Exception:
                # Si el elemento se volvió stale, buscar el botón de nuevo
                submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
                submit_button.click()
    except Exception as e:
        print(f"⚠ Error al ejecutar login: {e}")
        # Último intento: buscar el botón y hacer clic
        try:
            submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
            submit_button.click()
        except Exception as e2:
            # Si todo falla, usar JavaScript para hacer clic
            driver.execute_script("""
                var btn = document.querySelector('button[type="submit"]');
                if (btn) btn.click();
            """)
    
    time.sleep(2)
    
    # ============= 3. VALIDACIÓN ==============
    # Verificar si hay algún alert visible
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text
        print(f"⚠ ALERT DETECTADO: {alert_text}")
        alert.accept()
    except:
        pass
    
    # Esperar a que se complete el login (verificar token o cambio de URL)
    max_wait = 10
    elapsed = 0
    token = None
    current_url = driver.current_url
    
    while elapsed < max_wait:
        time.sleep(0.5)
        elapsed += 0.5
        
        token = driver.execute_script("return localStorage.getItem('token');")
        current_url = driver.current_url
        
        if token or "dashboard" in current_url.lower():
            break
    
    success = token is not None or "dashboard" in current_url.lower()
    
    return {
        'success': success,
        'token': token,
        'current_url': current_url
    }
