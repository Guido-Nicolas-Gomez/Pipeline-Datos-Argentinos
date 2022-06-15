# Pipline para datos.gob.ar
---
## Tabla de contenido:
1. [Descripcion del proyecto](#descripcion-del-proyecto)
    1. [Archivos fuente](#archivos-fuente)
    2. [Procesamiento de datos](#procesamiento-de-datos)
    3. [Creación de tablas / bbdd](#creación-de-tablas-y-bbdd)
    4. [Actualización de la bbdd](#actualización-de-la-bbdd)
2. [Variables de entorno](#variables-de-entorno)
3. [Crecion del entorno virtual y ejecucion](#creacion-del-entorno-virtual-y-ejecucion)
---
# Descripcion del proyecto
## Archivos fuente
Los archivos fuentes son utilizados en el proyecto para obtener de ellos todo lo
necesario para popular la base de datos.  
El proyecto:
- Obtiene los 3 archivos de fuente utilizando la librería requests y
almacenarse en forma local 
    - Datos Argentina - Museos
    - Datos Argentina - Salas de Cine
    - Datos Argentina - Bibliotecas Populares  
- Los archivos se organizan en rutas siguiendo la siguiente estructura:
“categoría\año-mes\categoria-dia-mes-año.csv”
    - Por ejemplo: “museos\2021-noviembre\museos-03-11-2021”
    - Si el archivo existe debe reemplazarse. La fecha de la nomenclatura
es la fecha de descarga.  
## Procesamiento de datos
El procesamiento de datos permite a nuestro proyecto transformar los datos de los
archivos fuente en la información que va a nutrir la base de datos. Para esto, el
proyecto:

- Normaliza toda la información de Museos, Salas de Cine y Bibliotecas
Populares, para crear una única tabla que contenga:
    - cod_localidad
    - id_provincia
    - id_departamento
    - categoría
    - provincia
    - localidad
    - nombre
    - domicilio
    - código postal
    - número de teléfono
    - mail
    - web
- Procesa los datos conjuntos para poder generar una tabla con la siguiente
información:
    - Cantidad de registros totales por categoría
    - Cantidad de registros totales por fuente
    - Cantidad de registros por provincia y categoría
- Procesa la información de cines para poder crear una tabla que contenga:
    - Provincia
    - Cantidad de pantallas
    - Cantidad de butacas
    - Cantidad de espacios INCAA  

## Creación de tablas y bbdd

Para disponibilizar la información obtenida y procesada en los pasos previos, el
proyecto crea una base de datos que cumple con los siguientes requisitos:
- Motor de bases de datos MySql
- Cuenta con los scripts .sql para la creación de las tablas.
- Un script .py que ejecuta los scripts .sql para facilitar el deploy.
- Los datos de la conexión se configuran fácilmente para facilitar
el deploy en un nuevo ambiente de ser necesario.

## Actualización de la bbdd
Luego de normalizar la información y generar las demás tablas, las mismas se actualizan en la base de datos:
- Todos los registros existentes son reemplazados por la nueva
información.
- Dentro de cada tabla se indica en una columna adicional la fecha de
carga.
- Los registros para los cuales la fuente no brinda información son cargados
como nulos.
---
# Variables de entorno
Creacion de las variables de entorno:
- En el directorio del proyecto, crear un archivo ___.env___
- En el mismo se deben crear las siguientes variables:
    - _urls (En caso que los links hayan cambiado, reemplazarlos)_
        - __URL_MUSEOS__ = 'https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/4207def0-2ff7-41d5-9095-d42ae8207a5d/download/museos_datosabiertos.csv'
        - __URL_CINES__ = 'https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/392ce1a8-ef11-4776-b280-6f1c7fae16ae/download/cine.csv'
        - __URL_BIBLIOTECAS__ = 'https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/01c6c048-dbeb-44e0-8efa-6944f73715d7/download/biblioteca_popular.csv'

    - _Variables de conexion_
        - __ENGINE__ = [motor de la base de datos]
        - __USER__ = [usuario de la base de datos]
        - __PASSWORD__ = [contraseña]
        - __HOST__ = [direccion http]
        - __PORT__ = [numero de puerto]
        - __DATA_BASE__ = [nombre de la base de datos]

- A su vez crear un archivo ___.gitignore___ para no incluir este archivo en el correspondiente repositorio

---
# Creacion del entorno virtual y ejecucion
Con la terminal ubicada en el directorio de nuestro proyecto, lo primero es crear el entorno virtual, preferentemente en una carpeta aparte:
>C:/Users/x_path/mi_project>
> `$ python -m venv venv`

Luego se procede con la activacion del entorno virtual:
>C:/Users/x_path/mi_project/venv/Scripts>
>`$ active`

Regresamos al directorio de nuestro proyecto e importan los requerimientos:
>C:/Users/x_path/mi_project>
>`$ pip install -r requirements.txt`

Finalmente, para la ejecucion, dentro del directorio pipeline ejecutar el script main.py:
>C:/Users/x_path/mi_project/pipeline>
>`$ python main.py`

