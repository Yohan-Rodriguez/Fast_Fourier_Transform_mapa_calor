import time

import numpy as np
import pandas as pd

import aux_functions as aux_func

from selenium import webdriver
from selenium.webdriver.common.by import By


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
    # driver = webdriver.Chrome(options=options)

    driver_path = "chromedriver-win64/chromedriver.exe"
    driver = webdriver.Chrome(options=options, executable_path=driver_path)


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
    
    # ================================================================================================================ #
    # CONN DRIVER                                                                                                      #
    # ================================================================================================================ #   
    # Iterar sobre cada una de las 19 jornadas
    for i_jornada in range(1, 3, 1):
        
        # Url de una jornada específica
        url_jor = 'https://resultados.as.com/resultados/futbol/colombia_i/2024/jornada/regular_a_{}/'.format(i_jornada)
        driver.get(url_jor) 
       
        # Obtener el html parse de la página de la jornada
        soup_rx = aux_func.parse_bs4(url_tx=url_jor)

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
        urls_matches_rx = [i_url.attrs['href'] for i_url in soup_rx.find_all('a', {'class': 'resultado'}) ]

        # Abrir cada uno de los links en una ventana nueva
        for i_urls_matches in urls_matches_rx[:3]:
            driver.execute_script("window.open('" + i_urls_matches + "');")

            # Obtiene los identificadores de las ventanas
            window_handles = driver.window_handles

            # Focalizar la iteracción sobre la nueva ventana 
            driver.switch_to.window(window_handles[1])

            # Buscar y presionar el botón de estadísticas
            print(i_urls_matches, type(i_urls_matches))
            soup_rx = aux_func.parse_bs4(url_tx=i_urls_matches)
            link_stats = soup_rx.find('a', {'data-item': 'stats'}).attrs['href']
            print('https://colombia.as.com{}'.format(link_stats))
            
            # Abrir página de estadísticas
            driver.get('https://colombia.as.com{}'.format(link_stats))

            # Scroll hacia el mapa de calor
            xptah_butt_heat_map = '/html/body/div[6]/article/section/div/div/div[1]/div[5]/div/div/h3'
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
      
            
            # # Buscar e ir hacia la sección del mapa de calor para que cargue adecuadamente
            # aux_func.search_and_click_on_button(driver=driver, xpath_tx=xptah_butt_heat_map, click_js=False)

            # Cierra la nueva ventana y regresa a la inicial
            time.sleep(np.random.randint(5, 7))
            driver.close()                      
            driver.switch_to.window(window_handles[0])

        time.sleep(np.random.randint(1, 3))

    # END --------- CONN DRIVER                                                                                        #
    # ================================================================================================================ # 


    # Cerrar navegador
    driver.quit()

    print('\nFIN...\n')
# END --------- MAIN                                                                                                   #
# ==================================================================================================================== #

get_data()