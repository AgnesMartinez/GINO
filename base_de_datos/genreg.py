import random
import sqlite3
import concurrent.futures
from datetime import date, datetime, timedelta

#Conexion BD Local
DEFAULT_PATH = "./base_de_datos/db.sqlite3"

def db_connect(db_path=DEFAULT_PATH):
    conn_local = sqlite3.connect(db_path)
    return conn_local

conn_local = db_connect()

#variables
fechahoy = date.today()
x = datetime.today()
tiempo = x.strftime("%H:%M")
catalogo = []
cantidad = 0
especialidad = ""
ligine = []
lipedia = []

#Materia prima para registros aleatorios
nombres_mujer = ['MARIA','JULIETA','SOFIA','ANDREA','PAOLA','ESPERANZA','FERNANDA']

apellidos = ['GARCIA','GONZALEZ','LOPEZ','PEREZ','HERNANDEZ','PEREZ','RODRIGUEZ','SANCHEZ','FLORES','GOMEZ']

servicio_gine = ['Urgencias GyO','Labor / Toco (GyO)','Quirofano GyO','Alojamiento Conjunto GyO','Modulo Mater']

servicio_pedia = ['Urgencias Pediatria','Labor / Toco (Pediatria)', 'Quirofano Pediatria','UCIN','Cunero Patologico','Cuidados Intermedios','Alojamiento Conjunto Pediatria']

fecha_nacimiento = ['2020/01/05','2020/01/10','2020/01/15','2020/01/25','2020-01-30',
                    '2020/02/05','2020/02/10','2020/02/15','2020/02/25','2020-02-28'
                    '2020/03/05','2020/03/10','2020/03/15','2020/03/25','2020-03-30'
                    '2020/04/05','2020/04/10','2020/04/15','2020/04/25','2020-04-30'
                    '2020/05/05','2020/05/10','2020/05/15','2020/05/25','2020-05-30'
                    '2020/06/05','2020/06/10','2020/06/15','2020/06/25','2020-06-30'
                    '2020/07/05','2020/07/10','2020/07/15','2020/07/25','2020-07-30'
                    '2020/08/05','2020/08/10','2020/08/15','2020/08/25','2020-08-30'
                    '2020/09/05','2020/09/10','2020/09/15','2020/09/25','2020-09-30'
                    '2020/10/05','2020/10/10','2020/10/15','2020/10/25','2020-10-30'
                    '2020/11/05','2020/11/10','2020/11/15','2020/11/25','2020-11-30'
                    '2020/12/05','2020/12/10','2020/12/15','2020/12/25','2020-12-30'
                    ]

sexo = ['H','M']


#Catalogo de insumos extraido de la BD Local
with conn_local:

    query = """SELECT clave,nombre FROM catalogoinsumos ORDER BY nombre"""

    lista = conn_local.execute(query)

    for item in lista:

        catalogo.append(item[0])

#Funciones
def generar_gine():

    nombre = f'{random.choice(nombres_mujer)} {random.choice(apellidos)} { random.choice(apellidos)}'
        
    nom_completo = nombre.upper().split()
        
    curp = f'{nom_completo[1][0:2]}{nom_completo[2][0:2]}{12345678}'
        
    servicio = random.choice(servicio_gine)

    fechazar = fechahoy - timedelta(days=random.randint(0,100))
        
    insumo = random.choice(catalogo)

    valores = (nombre,curp,insumo,fechazar,tiempo,servicio)

    ligine.append(valores)
    


def generar_pedia():
    
    nombre = f'RN {random.choice(apellidos)} { random.choice(apellidos)}'
        
    nom_completo = nombre.upper().split()
        
    curp = f'{nom_completo[1][0:2]}{nom_completo[2][0:2]}{12345678}'
        
    fena = random.choice(fecha_nacimiento)
        
    sexobebe = random.choice(sexo)

    CUPI = f'{nom_completo[1][0:2]}{nom_completo[2][0:2]}{fena[2:].replace("/","")}{sexobebe}'

    servicio = random.choice(servicio_pedia)

    insumo = random.choice(catalogo)

    fechazar = fechahoy - timedelta(days=random.randint(0,100))

    valores = (nombre,curp,CUPI,insumo,fechazar,tiempo,servicio)

    lipedia.append(valores)
    

def agregar_reg():

    if especialidad.upper() == "GINE":
        query = """INSERT INTO ginecologia (paciente_id,CURP,clave,fecha,hora,servicio) VALUES (?,?,?,?,?,?)"""
    
        with conn_local:
            conn_local.executemany(query,ligine)
    
    elif especialidad.upper() == "PEDIA":
        query = """INSERT INTO pediatria (paciente_id,CURP,CUPI,clave,fecha,hora,servicio) VALUES (?,?,?,?,?,?,?)"""
    
        with conn_local:
            conn_local.executemany(query,lipedia)


#Funcion principal
def main():
    
    print("- - - - - - - - - - -\n¿Estas buscando como registrar entradas de datos a granel?\n- - - - - - - - - - -\nVale! Yo me encargo, solo responde dos preguntitas:")

    global especialidad

    especialidad = input("\n¿En que especialidad quieres los registros? (gine o pedia):\n")

    global cantidad
    cantidad = int(input("\n¿Cuantos registros quieres?:\n"))

    if especialidad.upper() == "GINE":
        for i in range(cantidad):
            generar_gine()

    elif especialidad.upper() == "PEDIA":
        for i in range(cantidad):
            generar_pedia()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.submit(agregar_reg())
    
    print("\nEnhorabuena! Registros Exitosos,Ok,bye.")



if __name__ == "__main__":
    main()


    
