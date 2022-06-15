-- Volcando estructura de base de datos para bbdd
CREATE DATABASE IF NOT EXISTS bbdd;
USE bbdd;

-- Volcando estructura para tabla bbdd.info_1
CREATE TABLE IF NOT EXISTS info_1 (
  id int unsigned NOT NULL AUTO_INCREMENT,
  cod_localidad int unsigned DEFAULT NULL,
  id_provincia smallint unsigned DEFAULT NULL,
  id_departamento mediumint unsigned DEFAULT NULL,
  categoria varchar(150) DEFAULT NULL,
  provincia varchar(100) DEFAULT NULL,
  localidad varchar(100) DEFAULT NULL,
  nombre varchar(200) DEFAULT NULL,
  domicilio varchar(200) DEFAULT NULL,
  codigo_postal varchar(100) DEFAULT NULL,
  telefono varchar(50) DEFAULT NULL,
  mail varchar(150) DEFAULT NULL,
  web varchar(250) DEFAULT NULL,
  fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='Normalizar toda la información de Museos, Salas de Cine y Bibliotecas\r\nPopulares, para crear una única tabla que contenga:\r\n    - cod_localidad\r\n    - id_provincia\r\n    - id_departamento\r\n    - categoría\r\n    - provincia\r\n    - localidad\r\n    - nombre\r\n    - domicilio\r\n    - código postal\r\n    - número de teléfono\r\n    - mail\r\n    - web';

-- Volcando estructura para tabla bbdd.info_2
CREATE TABLE IF NOT EXISTS info_2 (
  id int unsigned NOT NULL AUTO_INCREMENT,
  provincia varchar(100) DEFAULT NULL,
  categoria varchar(150) DEFAULT NULL,
  fuente varchar(150) DEFAULT NULL,
  registros_categoria smallint unsigned NOT NULL DEFAULT '0',
  registros_fuente smallint unsigned NOT NULL DEFAULT '0',
  registros_prov_cat smallint unsigned NOT NULL DEFAULT '0',
  fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='Procesar los datos conjuntos para poder generar una tabla con la siguiente\r\ninformación:\r\n- Cantidad de registros totales por categoría\r\n- Cantidad de registros totales por fuente\r\n- Cantidad de registros por provincia y categoría';

-- Volcando estructura para tabla bbdd.info_3
CREATE TABLE IF NOT EXISTS info_3 (
  id smallint unsigned NOT NULL AUTO_INCREMENT,
  provincia varchar(100) DEFAULT NULL,
  pantallas smallint unsigned NOT NULL DEFAULT '0',
  butacas mediumint unsigned NOT NULL DEFAULT '0',
  espacios_INCAA tinyint unsigned NOT NULL DEFAULT '0',
  fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='Procesar la información de cines para poder crear una tabla que contenga:\r\n- Provincia\r\n- Cantidad de pantallas\r\n- Cantidad de butacas\r\n- Cantidad de espacios INCAA';
