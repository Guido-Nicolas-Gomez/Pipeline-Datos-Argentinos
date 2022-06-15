import pandas as pd
from sqlalchemy import create_engine
from decouple import config
from tools import * 

if __name__ == '__main__':
# Obtencion de Variables de Entorno
    try:
        logger.info("Se procede a leer las variables de entorno")
        # urls
        URL_MUSEOS = config('URL_MUSEOS')
        URL_CINES = config('URL_CINES')
        URL_BIBLIOTECAS = config('URL_BIBLIOTECAS')
        # Variables de conexion
        ENGINE = config('ENGINE')
        USER = config('USER')
        PASSWORD = config('PASSWORD')
        HOST = config('HOST')
        PORT = config('PORT')
        DATA_BASE = config('DATA_BASE')
    except:
        logger.error("Revisar las variables de entorno, el archivo no esta creado correctamente, o faltan variables")
        raise Exception("Revisar las variables de entorno, el archivo no esta creado correctamente, o faltan variables")


    # Consulta, almacenado y carga de los datasets
    try:
        logger.info("Se procede a recuperar la informacion del las urls, guardarlas y leerlas en un dataframe")
        # Dataframes
        df_museos = requests_writing_reading('museos', URL_MUSEOS)
        df_cines = requests_writing_reading('cines', URL_CINES)
        df_bibliotecas = requests_writing_reading('bibliotecas', URL_BIBLIOTECAS)
    except:
        logger.error("Error en la lectura de los archivos")
        raise Exception("Error en la lectura de los archivos")


    # Limpieza de los datasets
    # Para utilizar posteriormente
    logger.info("Se inicia limpieza y modificacion de los dataset, para generar los datos solicitados")
    df_cines_copy = df_cines.copy()

    # Unificando numero de telefono y codigo de area:
    df_museos.insert(13, 'telef.', concat_float_and_str_columns(df_museos, 'cod_area', 'telefono'))
    df_cines.insert(13, 'telef.', concat_float_and_str_columns(df_cines, 'cod_area', 'Teléfono'))
    df_bibliotecas.insert(13, 'telef.', concat_float_and_str_columns(df_bibliotecas, 'Cod_tel', 'Teléfono'))

    # Drop columns
    columns_to_drop_museos = ['cod_area','telefono','Observaciones', 'subcategoria','piso','Latitud','Longitud', 'TipoLatitudLongitud','Info_adicional']
    columns_to_drop_cines = ['cod_area','Teléfono','Observaciones', 'Departamento','Piso','Información adicional','Latitud','Longitud','TipoLatitudLongitud']
    columns_to_drop_bibliotecas = ['Cod_tel','Teléfono','Observacion', 'Subcategoria','Departamento','Piso','Información adicional','Latitud','Longitud', 'TipoLatitudLongitud']

    # Eliminando las columnas innecesarías
    df_museos = df_museos.drop(columns_to_drop_museos, axis=1)
    df_cines = df_cines.drop(columns_to_drop_cines, axis=1)
    df_bibliotecas = df_bibliotecas.drop(columns_to_drop_bibliotecas, axis=1)


    # Creacion del dataset unificado
    # Columnas necesarias
    columns = ['cod_localidad',
            'id_provincia',
            'id_departamento',
            'categoria',
            'provincia',
            'localidad',
            'nombre',
            'domicilio',
            'codigo_postal',
            'telefono',
            'mail',
            'web',
            'fuente',]

    # Concatenamiento en un solo dataset
    df_main = pd.DataFrame()
    for i, v in enumerate(columns):
        df_main[v] = pd.concat([df_museos.iloc[:,i], df_cines.iloc[:,i], df_bibliotecas.iloc[:,i]])


    # Tabla N° 1
    # Tabla solo con los campos especificados, (se excluje 'fuente')
    df_info_1 = df_main.iloc[ : , :-1]


    # Tabla N° 2
    # Campos requeridos de la tabla base
    df_info_2 = df_main[['provincia', 'categoria', 'fuente']]

    # Datasets agrupados por catagoría, fuente y provincia.
    df_count_categoria = df_main.groupby('categoria').count()['cod_localidad']
    df_count_fuente = df_main.groupby('fuente').count()['cod_localidad']
    df_count_provincia_categoria = df_main.groupby(['provincia','categoria']).count()['cod_localidad']

    # Datos agrupados que seran agragados a la tabla maestra
    data_to_agregate = [(df_count_categoria, 'categoria', 'registros_categoria'),
                        (df_count_fuente, 'fuente', 'registros_fuente'),
                        (df_count_provincia_categoria, ['provincia', 'categoria'], 'registros_prov_cat'),]

    # Agregacion de la informacion
    for data in data_to_agregate:
        df_info_2 = pd.merge(left= df_info_2, right= data[0], how= 'left', on= data[1])
        df_info_2 = df_info_2.rename(columns= {'cod_localidad': data[2]})


    # Tabla N° 3
    # Nueva lectura de cines
    df_cines = df_cines_copy

    # Convertir en valores numericos el recuento espacio_INCAA
    df_cines['espacio_INCAA'] = df_cines['espacio_INCAA'].transform(lambda x: 1 if x == 'si' or x == 'SI' else 0)

    # Creando la tabla agrupada por provincia
    columns = ['Provincia', 'Pantallas', 'Butacas', 'espacio_INCAA']
    df_info_3 = df_cines[columns].groupby('Provincia').sum()
    df_info_3 = df_info_3.rename(columns= {'espacio_INCAA':'espacios_INCAA'})
    df_info_3['Provincia'] = df_info_3.index


    # Creacion de la base de datos
    # Connection string for the engine
    CONNECTION_STRING = ENGINE + '://' + USER + ':' + PASSWORD + '@' + HOST + ':' + PORT
    # creacion del motor
    engine = create_engine(CONNECTION_STRING)#, echo= True)

    try:
        logger.info("Realizando la coneccion con la base de datos")
        # Creacion de la base de datos y las tablas
        with engine.connect() as con:
            with open('bbdd.sql', 'r') as f:
                con.execute(f.read())
    except:
        logger.error('No se puedo conectar con la base de datos, revisar variables de entorno')
        raise Exception('No se puedo conectar con la base de datos, revisar variables de entorno')

    # Se agrega el nombre de la base de datos al engine para agregar los datos a las tablas
    engine = create_engine(CONNECTION_STRING + '/' + DATA_BASE)

    # Actualizado valores en la base de datos:
    for i, df in enumerate([df_info_1, df_info_2, df_info_3]):
        logger.info(f'Iniciando la escritura de la tabla info_{i + 1}')
        try:
            # Borrado de los datos previos
            with engine.connect() as con:
                con.execute(f'DELETE FROM info_{i + 1}')
            # Carga de los nuevos datos
            df.to_sql(f'info_{i + 1}',con = engine, index = False, if_exists = 'append', method=  'multi')
        except:
            logger.error(f'Error al intentar cargar datos en tabla info_{i + 1}')
    logger.info('FIN DE LA EJECUCION DEL PROGRAMA')