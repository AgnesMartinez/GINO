import pymysql.cursors
import csv

def maria_connect():
    try:
        conn = pymysql.connect(
            user="root",
            password="pruebas",
            host="localhost",
            port=3306
        )
        
        return conn

    except Exception as e:
        print(f"Error connecting to MariaDB Platform: {e}")

conn_maria = maria_connect()

cursor = conn_maria.cursor()

#Crear base de datos
bd_maria = """CREATE DATABASE IF NOT EXISTS hmi"""
usar_maria = """USE hmi"""

cursor.execute(bd_maria)

cursor.execute(usar_maria)

#Catalogo de insumos con clave como indice
catalogoinsumos = """CREATE TABLE IF NOT EXISTS catalogoinsumos(
    ID INTEGER AUTO_INCREMENT,
    clave VARCHAR(255),
    nombre VARCHAR(255),
    descripcion TEXT,
    PRIMARY KEY (ID)
    )"""

cursor.execute(catalogoinsumos)

ind_clave = """CREATE INDEX IF NOT EXISTS ind_clave ON catalogoinsumos (clave)"""

cursor.execute(ind_clave)

#Crear tabla de pacientes para ginecologia
pacientes_ginecologia = """CREATE TABLE IF NOT EXISTS pacientes_gine ( 
    ID INTEGER AUTO_INCREMENT,
    nombre VARCHAR(255),
    CURP VARCHAR(255),
    status VARCHAR(255),
    PRIMARY KEY (ID)
    )"""

cursor.execute(pacientes_ginecologia)

ind_pxgine = """CREATE INDEX IF NOT EXISTS ind_pxgine ON pacientes_gine (CURP)"""

cursor.execute(ind_pxgine)

#Crear tabla de registros para ginecologia

registros_ginecologia = """CREATE TABLE IF NOT EXISTS registros_gine (
    ID INTEGER AUTO_INCREMENT,
    CURP VARCHAR (255) ,
    clave VARCHAR(255) ,
    fecha DATE ,
    hora VARCHAR(255) ,
    servicio VARCHAR(255),
    PRIMARY KEY (ID)
    )"""

cursor.execute(registros_ginecologia)

ind_gine = """CREATE INDEX IF NOT EXISTS ind_gine ON registros_gine (CURP)"""

cursor.execute(ind_gine)

#Crear tabla de pacientes para pediatria

pacientes_pediatria = """CREATE TABLE IF NOT EXISTS pacientes_pedia ( 
    ID INTEGER AUTO_INCREMENT,
    nombre VARCHAR(255),
    CURP VARCHAR(255),
    status VARCHAR(255),
    PRIMARY KEY (ID)
    )"""

cursor.execute(pacientes_pediatria)

ind_pxpedia = """CREATE INDEX IF NOT EXISTS ind_pxpedia ON pacientes_pedia (CURP)"""

cursor.execute(ind_pxpedia)

#Crear tabla de registros para pediatria

registros_pediatria = """CREATE TABLE IF NOT EXISTS registros_pedia (
    ID INTEGER AUTO_INCREMENT,
    CURP VARCHAR (255) ,
    clave VARCHAR(255) ,
    fecha DATE ,
    hora VARCHAR(255) ,
    servicio VARCHAR(255),
    PRIMARY KEY (ID)
    )"""

cursor.execute(registros_pediatria)

ind_pedia = """CREATE INDEX IF NOT EXISTS ind_pedia ON registros_pedia (CURP)"""

cursor.execute(ind_pedia)

#Crear usuarios
query= """CREATE USER IF NOT EXISTS 'agnesm'@localhost IDENTIFIED BY 'toor'"""

query2= """GRANT ALL PRIVILEGES ON *.* TO 'agnesm'@localhost IDENTIFIED BY 'toor'"""

cursor.execute(query)

cursor.execute(query2)


#agregar los datos del CSV a la base de datos
with open('./base_de_datos/catalogo.csv','r',encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    i = 0
    for row in csv_reader:
        if i == 0:
            i += 1
        else:
            clave = row[0]
            nombre = row[1]
            descripcion = row[2]
            valores = (clave,nombre,descripcion)
            insertar = """INSERT INTO catalogoinsumos (clave,nombre,descripcion) VALUES (%s,%s,%s)"""
            cursor.execute(insertar,valores)
            i += 1
            print(f'{i} - {row}\n===========\n')

conn_maria.commit()

conn_maria.close()