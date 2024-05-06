import time
import base64

from bs4 import BeautifulSoup
import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ==================================================================================================================== #
# SEARCH BUTTON                                                                                                        #
# ==================================================================================================================== #
def search_and_click_on_button(driver, xpath_tx, click_js=True):
    element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, xpath_tx)))

    # Clic sobre el elemtno encontrado por medio de script javascript
    if click_js:
        driver.execute_script("arguments[0].click();", element)    
    else:
        element.click()
# END ---------  SEARCH BUTTON                                                                                         #
# ==================================================================================================================== #
        

# ==================================================================================================================== #
# SELECT TEAM IN HEAT MAP                                                                                              #
# ==================================================================================================================== #
def select_teams_heat_map(driver, xpath_button_rx, xpath_radio_button_rx):
    search_and_click_on_button(driver, xpath_tx=xpath_button_rx)
    time.sleep(1)
    search_and_click_on_button(driver, xpath_tx=xpath_radio_button_rx)
    time.sleep(1)
    search_and_click_on_button(driver, xpath_tx=xpath_button_rx)
    time.sleep(1)
# END ---------  SELECT TEAM IN HEAT MAP                                                                               #
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


# ==================================================================================================================== #
# EXTRACT DATA IMG                                                                                                     #
# ==================================================================================================================== #
def extract_img(driver, i_jornada=None, home=None, away=None, home_or_away=None):

    time.sleep(2)

    # Imagen del mapa de calor
    xpath_img_heat_map = '//*[@id="Opta_0-heatmap-canvas"]'
    canvas_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, xpath_img_heat_map)))

    # Parsear el canvas de la imagen como un string base64 para obtener su representación en texto
    image_data_base64 = driver.execute_script("""
        var canvas = arguments[0];
        var imageData = canvas.toDataURL('image/png');
        return imageData;""", 
        canvas_element)

    # Decode the base64 string into image bytes
    image_bytes = base64.b64decode(image_data_base64.split(',')[1])

    # Guardar imagen
    with open('Img/{}_{}_{}_{}.png'.format(i_jornada, home, away, home_or_away), "wb") as image_file:
        image_file.write(image_bytes)
# END ---------  EXTRACT DATA IMG                                                                                      #
# ==================================================================================================================== #
        