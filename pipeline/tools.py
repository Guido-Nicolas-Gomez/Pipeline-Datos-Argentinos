# Modulos
import datetime
import locale
import os
import logging
import requests
import pandas as pd

# Configuracion de logging
logging_path = os.path.abspath(os.getcwd()) + "/logging_info.log"
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = logging_path,
                    level = logging.DEBUG,
                    format = LOG_FORMAT,
                    filemode = 'w')
logger = logging.getLogger()


# Peticion y carga de los ficheros
def requests_writing_reading(name, url): #from url to data frame
    # variables
    #   time
    locale.setlocale(locale.LC_ALL, 'es-ES')
    dt = datetime.datetime.now()
    current_month = dt.strftime('%Y-%B')
    today = dt.strftime('%d-%m-%Y')
    #   paths
    main_path = os.path.abspath(os.getcwd())
    file_dir = fr'{name}\{current_month}'
    file_name = f'/{name}-{today}.csv'
    fullpath = os.path.join(main_path, file_dir + file_name)
    
    # making dir
    logger.info(f"Se procede a crear los directorios {file_dir}")
    os.makedirs(file_dir, exist_ok= True)

    # requests
    try:
        r = requests.get(url)
    except:
        logger.error(f'Error de conexion a la url: {url}\n Error code: {r.status_code}')

    # Storage
    logger.info(f"Se procede a crear/sobreescribir el archivo {file_name[1:]}")
    with open(fullpath, 'w', encoding="latin-1") as f: #unicode
        f.write(r.text.replace('\r',''))
    
    # Reading
    return pd.read_csv(fullpath)

# Unificando numero de telefono y codigo de area:
def concat_float_and_str_columns(df, float_column, str_column):
    """Funcion que concatena dos columnas en un dataframe, una correspondiente a tipo Str y otra a Float"""
    float_to_str = lambda x: str(x)[:-2]
    concat_columns = df[float_column].agg(float_to_str) + ' ' + df[str_column]
    return concat_columns.str.strip()