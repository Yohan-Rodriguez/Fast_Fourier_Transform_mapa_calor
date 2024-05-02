import time

from bs4 import BeautifulSoup
import requests

import numpy as np
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ==================================================================================================================== #
# SEARCH MATCHE'S URL                                                                                                  #
# ==================================================================================================================== #
def search_urls_matches_jor(url):
    """
    Obtener las url's de los 10 partdis encada una de las 19 jornadas

    Args:

    Returns:
        driver: Conección con el el navagador web

    Examples:     
    """

    # Realizar solicitud HTTP a la URL
    url = 'https://resultados.as.com/resultados/futbol/colombia_i/2024/jornada/regular_a_1/'

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

    '''
    Obtener las 10 url's de los partidos de la jornada:
    
    ej:
    urls_matches = ['https://colombia.as.com/futbol/jaguares-abre-la-liga-con-victoria-ante-patriotas-n/',
                    'https://colombia.as.com/futbol/partidazo-y-golazos-en-el-empate-entre-pereira-y-cali-n/',
                    ...
                    ...
                    ...
                    'https://colombia.as.com/futbol/equidad-y-envigado-sin-efectividad-en-techo-n/',
                    'https://colombia.as.com/futbol/santa-fe-gana-en-su-debut-triunfo-ante-pasto-con-gol-de-rodallega-n/']
    '''
    urls_matches = [i_url.attrs['href'] for i_url in soup.find_all('a', {'class': 'resultado'}) ]
    print(urls_matches)

    return urls_matches
# END ---------  SEARCH MATCHE'S URL                                                                                   #
# ==================================================================================================================== #


# ==================================================================================================================== #
# CHROME DRIVER CONNECTION                                                                                             #
# ==================================================================================================================== #
def inicializar_driver():
    """
    Crear la conexión con el navegador web BRAVE para la tarea automatizada

    Args:

    Returns:
        driver: Conección con el el navagador web

    Examples:     
    """
    options = webdriver.ChromeOptions()
    options.binary_location = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'
    driver = webdriver.Chrome(options=options)

    return driver
# END --------- CHROME DRIVER CONNECTION                                                                               #
# ==================================================================================================================== #


# ==================================================================================================================== #
# MAIN                                                                                                                 #
# ==================================================================================================================== #
def get_data():
    """
    Función principal. Crear el WebDriver y abre el navegador
    
    Args:
        No

    Returns:
        No

    Examples:
        >>> get_data()

        >>> get_data()
    """

    # ================================================================================================================ #
    # CONN DRIVER                                                                                                      #
    # ================================================================================================================ #   

    # Inicializar el driver
    driver = inicializar_driver()

    # Abrir navegador
    driver.maximize_window()
      
    # END --------- CONN DRIVER                                                                                        #
    # ================================================================================================================ # 
    
    for i_jornada in range(1, 3, 1):

        url_jor = 'https://resultados.as.com/resultados/futbol/colombia_i/2024/jornada/regular_a_{}/'.format(i_jornada)
        driver.get(url_jor) 
       
        urs_matches = search_urls_matches_jor(url=url_jor)

        for i_urls_matches in urs_matches[:3]:
            print(i_urls_matches)
            driver.execute_script("window.open('" + i_urls_matches + "');")
            
            time.sleep(np.random.randint(1, 3))
            driver.close()

        time.sleep(np.random.radint(1, 3))



    # Cerrar navegador
    driver.quit()

    print('\nFIN...\n')
# END --------- MAIN                                                                                                   #
# ==================================================================================================================== #

get_data()