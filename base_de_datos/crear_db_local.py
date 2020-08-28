import sqlite3
import csv


#conectar a base de datos local
DEFAULT_PATH = "./base_de_datos/db.sqlite3"

def db_connect(db_path=DEFAULT_PATH):
    conn_local = sqlite3.connect(db_path)
    return conn_local

conn_local = db_connect()

#iniciar cursor para querys
cur = conn_local.cursor()

#Crear tablas basicas 

#Catalogo de insumos con clave como indice
catalogoinsumos = """CREATE TABLE IF NOT EXISTS catalogoinsumos (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    clave VARCHAR(255),
    nombre VARCHAR(255),
    descripcion text)"""

cur.execute(catalogoinsumos)

ind_clave = """CREATE INDEX IF NOT EXISTS ind_clave ON catalogoinsumos (clave)"""

cur.execute(ind_clave)

#Crear tabla de pacientes para ginecologia
pacientes_ginecologia = """CREATE TABLE IF NOT EXISTS pacientes_gine ( 
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(255),
    CURP VARCHAR(255),
    status VARCHAR(255) 
    )"""

cur.execute(pacientes_ginecologia)

ind_pxgine = """CREATE INDEX IF NOT EXISTS ind_pxgine ON pacientes_gine (CURP)"""

cur.execute(ind_pxgine)

#Crear tabla de registros para ginecologia

registros_ginecologia = """CREATE TABLE IF NOT EXISTS registros_gine (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    CURP VARCHAR (255) ,
    clave VARCHAR(255) ,
    fecha DATE ,
    hora VARCHAR(255) ,
    servicio VARCHAR(255),
    synced INTEGER DEFAULT 0)"""

cur.execute(registros_ginecologia)

ind_gine = """CREATE INDEX IF NOT EXISTS ind_gine ON registros_gine (CURP)"""

cur.execute(ind_gine)

#Crear tabla de pacientes para pediatria

pacientes_pediatria = """CREATE TABLE IF NOT EXISTS pacientes_pedia ( 
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(255),
    CURP VARCHAR(255),
    status VARCHAR(255)
    )"""

cur.execute(pacientes_pediatria)

ind_pxpedia = """CREATE INDEX IF NOT EXISTS ind_pxpedia ON pacientes_pedia (CURP)"""

cur.execute(ind_pxpedia)

#Crear tabla de registros para pediatria

registros_pediatria = """CREATE TABLE IF NOT EXISTS registros_pedia (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    CURP VARCHAR (255) ,
    clave VARCHAR(255) ,
    fecha DATE ,
    hora VARCHAR(255) ,
    servicio VARCHAR(255),
    synced INTEGER DEFAULT 0)"""

cur.execute(registros_pediatria)

ind_pedia = """CREATE INDEX IF NOT EXISTS ind_pedia ON registros_pedia (CURP)"""

cur.execute(ind_pedia)

print(cur.fetchall())

#agregar los datos del CSV a la base de datos
with open('./base_de_datos/catalogo.csv','r',encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    i = 0
    for row in csv_reader:
        if i == 0:
            i += 1
        else:
            insertar = """INSERT INTO catalogoinsumos (clave,nombre,descripcion) VALUES (?,?,?)"""
            cur.execute(insertar,row)
            i += 1

            print(f'{i} - {row}')

conn_local.commit()

conn_local.close()