import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from tests.utils.auth_helpers import find_chromium_binary, login


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
    
    # Intentar usar Chromium si está disponible
    chromium_path = find_chromium_binary()
    if chromium_path:
        options.binary_location = chromium_path

    # Instalar y usar automáticamente el chromedriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    yield driver  # aquí se ejecuta el test

    # Teardown: cerrar navegador
    driver.quit()


def test_project_phase_selection(driver):
    """
    Prueba de aceptación:
    1. Ingresar al sistema
    2. Seleccionar un proyecto con el botón project-select
    3. Cambiar la fase del proyecto con el botón phase-select
    """

    # ============= 1. PREPARACIÓN DE LA PRUEBA =============
    wait = WebDriverWait(driver, 10)
    
    # Paso 1: Ingresar al sistema
    login_result = login(driver, username="AnaMartinez", password="1234")
    
    # Validar que el login fue exitoso
    assert login_result['success'], f"El login falló. URL actual: {login_result['current_url']}"
    
    # Esperar a que la página del dashboard cargue
    time.sleep(2)

    # ============= 2. LÓGICA DE LA PRUEBA ==================
    
    # Paso 2: Seleccionar un proyecto con el botón project-select
    project_select = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='project-select']")))
    
    # Verificar que el selector tiene opciones disponibles
    select_project = Select(project_select)
    options = select_project.options
    
    # Verificar que hay al menos una opción (excluyendo la opción por defecto)
    assert len(options) > 1, "No hay proyectos disponibles para seleccionar"
    
    # Seleccionar la primera opción que no sea la opción por defecto
    for option in options:
        if option.get_attribute('value') and option.get_attribute('value') != '':
            select_project.select_by_value(option.get_attribute('value'))
            print(f"[OK] Proyecto seleccionado: {option.text}")
            break
    
    # Esperar a que se cargue la información del proyecto
    time.sleep(1)
    
    # Paso 3: Cambiar la fase del proyecto con el botón phase-select
    phase_select = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='phase-select']")))
    
    select_phase = Select(phase_select)
    phase_options = select_phase.options
    
    # Verificar que hay opciones de fase disponibles
    assert len(phase_options) > 0, "No hay fases disponibles para seleccionar"
    
    # Seleccionar una fase (evitar "Todas" que es null, seleccionar la primera fase real)
    phase_selected = False
    valid_phases = ['preparacion', 'cimentacion', 'obra_gruesa', 'obra_fina', 'inspeccion']
    
    for phase_option in phase_options:
        phase_value = phase_option.get_attribute('value')
        # Verificar que el valor no sea None, null, vacío, o "Todas"
        if phase_value and phase_value.lower() in valid_phases:
            select_phase.select_by_value(phase_value)
            print(f"[OK] Fase seleccionada: {phase_option.text}")
            phase_selected = True
            break
    
    # Si no se encontró una fase válida, intentar seleccionar por índice (saltando la primera que es "Todas")
    if not phase_selected and len(phase_options) > 1:
        select_phase.select_by_index(1)  # Índice 1 para saltar "Todas" (índice 0)
        print(f"[OK] Fase seleccionada: {phase_options[1].text}")
        phase_selected = True
    
    # Esperar 2 segundos como se solicitó
    time.sleep(2)

    # ============= 3. VALIDACIÓN / ACEPTACIÓN ==============
    # Verificar que los selectores están presentes y tienen valores seleccionados
    current_project = select_project.first_selected_option.get_attribute('value')
    current_phase = select_phase.first_selected_option.get_attribute('value')
    
    print(f"\nProyecto actual seleccionado: {current_project}")
    print(f"Fase actual seleccionada: {current_phase}")
    
    assert current_project is not None and current_project != '', "No se seleccionó ningún proyecto"
    assert phase_selected, "No se pudo seleccionar ninguna fase válida"
    assert current_phase is not None and current_phase != '', "No se seleccionó ninguna fase"
    
    print("\n[OK] Test completado exitosamente: Login, seleccion de proyecto y cambio de fase")

