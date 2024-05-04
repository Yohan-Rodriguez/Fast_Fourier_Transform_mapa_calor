import time


import numpy as np
import pandas as pd

import aux_functions as aux_func

from selenium import webdriver


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

        # Diccionario con la data de cada partido en particular
        dict_jornada = {'JOR': [], 'HOME': [], 'AWAY': [], 'G_H': [], 'G_A': [], 'stats_names': [],
                        'stats_match_H': [], 'stats_match_A': []}
        
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

            '''
            Buscar y acceder a la sección de "estadísticas"
            '''
            soup_rx = aux_func.parse_bs4(url_tx=i_urls_matches)
            link_stats = soup_rx.find('a', {'data-item': 'stats'}).attrs['href']            
            # Url de la página de las estadísticas del partido
            url_stats = 'https://colombia.as.com{}'.format(link_stats)            
            # Abrir página de estadísticas
            driver.get(url_stats)

            '''
            Data general
            '''
            soup_stats = aux_func.parse_bs4(url_tx=url_stats)
            
            # Nombre de los equipos del partido
            names_teams = [ i_team.get_text() for i_team in soup_stats.find_all('span', {'class': 'large'}) ]
            # Ej: ['Rionegro ▒guilas', 'Once Caldas']
            
            # # Goles en el partido
            # goals_teams = [ i_goal.get_text() for i_goal in soup_stats.find_all('div', {'class': 'scorers'}) ]
            # # Ej: ["Jorge Cardona 21' (pp)", "Jorge Cardona 58'"]
            
            # # Estadísticas:
            # # Labels de las estadísticas
            # stats_names = [ i_names_stats.get_text() for i_names_stats in soup_stats.find_all('h4', {'class': 'stat-tl'}) ]
            # # Ej: ['Disparos recibidos', 'Tarjetas amarillas', ... ,  'Fueras de juego', 'Disparos recibidos bloqueados']
            
            # # Estadísticas de los 2 equipos
            # stats_teams = [ i_home_stats.get_text() for i_home_stats in soup_stats.find_all('span', {'class': 'stat-val'}) ]
            # # Ej: ['58.6%', '41.4%', '7', '10', '4', ..., '3', '2', '1', '2']
            
            # '''
            # Alimentar el diccionario de partidos de la jornada
            # '''
            # dict_jornada['JOR'].append(i_jornada)
            # dict_jornada['HOME'].append(names_teams[0])
            # dict_jornada['AWAY'].append(names_teams[1])
            # dict_jornada['G_H'].append(goals_teams[0])
            # dict_jornada['G_A'].append(goals_teams[1])
            # dict_jornada['stats_names'].append( [stats_names] )
            # dict_jornada['stats_match_H'].append( [ stats_teams[enu] for enu in range(len(stats_teams)) if enu %2 == 0 ] )
            # dict_jornada['stats_match_A'].append( [ stats_teams[enu] for enu in range(len(stats_teams)) if enu %2 != 0 ] )

            '''
            Mapa de calor
            '''
            # Scroll hacia la sección del mapa de calor
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")

            aux_func.extract_img(driver=driver, i_jornada=i_jornada, home=names_teams[0], away=names_teams[1])

        #     # Cierra la nueva ventana y regresa a la inicial
        #     time.sleep(np.random.randint(5, 7))
        #     driver.close()                      

        #     # Foco sobre la ventan principal
        #     driver.switch_to.window(window_handles[0])

        
        # # Crear Datasframe con los 10 partidos de la joranda actual
        # df = pd.DataFrame(dict_jornada)

        # # Guardar DataFrame
        # df.to_csv('df_s/jornada_{}.csv'.format(i_jornada), encoding='latin',  index=False)

        time.sleep(np.random.randint(1, 3))

    # END --------- CONN DRIVER                                                                                        #
    # ================================================================================================================ # 


    # Cerrar navegador
    driver.quit()

    print('\nFIN...\n')
# END --------- MAIN                                                                                                   #
# ==================================================================================================================== #

get_data()