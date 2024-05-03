from bs4 import BeautifulSoup
import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ==================================================================================================================== #
# SEARCH BUTTON                                                                                                        #
# ==================================================================================================================== #
def search_and_click_on_button(driver, xpath_tx, click_js=True):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_tx)))

    # Clic sobre el elemtno encontrado por medio de script javascript
    if click_js:
        driver.execute_script("arguments[0].click();", element)    
    else:
        element.click()
# END ---------  SEARCH BUTTON                                                                                         #
# ==================================================================================================================== #
        

# ==================================================================================================================== #
# SEARCH MATCHE'S URL                                                                                                  #
# ==================================================================================================================== #
def parse_bs4(url_tx):
    """
    Obtener las url's de los 10 partdis encada una de las 19 jornadas

    Args:

    Returns:
        driver: Conección con el el navagador web

    Examples:     
    """

    # Realizar solicitud HTTP a la URL
    url = url_tx

    response = requests.get(url)

    # Código del estatdus de conexión
    status_code = response.status_code

    # Verificar el estado de la conexión a la página
    if status_code == 200:
        print('\nConexión establecida con éxito...')

    else:
        print('Error al establecer la conexión\nCódigo obtenido {}...'.format(status_code))

    # Obtener la estructura HTML de la página
    content = response.content

    '''
    BeautifulSoup: Parsear HTML y extraer data
    '''
    # Intsancia del BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')



    return soup
# END ---------  SEARCH MATCHE'S URL                                                                                   #
# ==================================================================================================================== #