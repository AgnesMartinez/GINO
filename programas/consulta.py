import PySimpleGUI as sg

sg.ChangeLookAndFeel('GreenTan')

#Menu
menuprincipal = [
    ['Reportes', ['Existencias de inventario por servicio']],
    ['Exportar',['Excel','Word']],
    ['Ayuda', ['Instrucciones','Acerca de...']], 
]

AreaResultados = [
    [sg.Multiline(size=(130,20),disabled=True,key='-output-')]
]


Info_Paciente = [
    [sg.Text('Nombre del paciente'), sg.Input(size=(40,2), key='-nombre-'),sg.Text('CURP'), sg.Input(size=(20,2), key='-curp-')],
    [ sg.Text('Servicio'), 
     sg.Combo(['Urgencias GyO','Labor / Toco (GyO)','Quirofano GyO','Alojamiento Conjunto GyO','Modulo Mater','Urgencias Pediatria',
    'Labor / Toco (Pediatria)', 'Quirofano Pediatria','UCIN','Cunero Patologico','Cuidados Intermedios',
    'Alojamiento Conjunto Pediatria'], size=(25,12), readonly=True, key='-servicio-'), sg.CalendarButton('Fecha de Nacimiento', target=(1,3), auto_size_button=True, format='%Y/%m/%d'), 
     sg.Input(size=(13,2), key='-fn-'), sg.Radio('Masculino', "RADIO1",key='-masc-'), sg.Radio('Femenino', "RADIO1",default=True, key='-fem-'),sg.Button('Buscar Registros')]
]

# Crear una lista con todas las pestañas
tabs = [
    [sg.TabGroup([
        [sg.Tab('Busqueda por paciente', Info_Paciente)]
        ]
        )
    ]
]


# Acomodo de elementos de ventana
layout = [
    [sg.Menu(menuprincipal, tearoff=True)],
    [sg.Frame('Resultados', AreaResultados)],
    [sg.Frame('Herramientas de Busqueda', tabs)]
]


#Ventana
window = sg.Window('HMI - Consulta de datos', layout)

#Parte funcional de la aplicacion

while True:  # Mantenerla persistente

    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

