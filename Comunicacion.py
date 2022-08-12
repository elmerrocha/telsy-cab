## Fundación Cardiovascular de Colombia
## Proyecto falla cardiaca
## v0.1 11/01/2021 03:00 p.m.

from serial import Serial
from time import sleep
import Metodo

puerto  = Serial('/dev/ttyAMA1', 115200)

def Leer(parametro):
    """ Lee los datos enviados por la tarjeta """
    Param = Metodo.Parametro(parametro)
    Long = Metodo.Longitud(parametro)
    Salida = []

    if(Long != 0):
        paquete = []
        for _ in range(0, Long):
            Dato_serial = Metodo.Convertir(puerto.read())
            paquete.append(Dato_serial)
    
    if   (parametro == 0x02):
        Salida = Metodo.ECG(paquete)
    elif (parametro == 0x03):
        Salida = Metodo.NIBP(paquete)
    elif (parametro == 0x04):
        Salida = Metodo.SPO2(paquete)
    elif (parametro == 0x05):
        Salida = Metodo.Temperatura(paquete)
          
    return [Param,Salida]

def Escribir(comando):
    """ Envía datos de configuración a la tarjeta """

    Comandos = {
        ######### Detección ECG
        1  : [b'\x55', b'\xAA', b'\x04', b'\x01', b'\x00', b'\xFA'], #Deshabilitar
        2  : [b'\x55', b'\xAA', b'\x04', b'\x01', b'\x01', b'\xF9'], #Habilitar
        ######### Detección NIBP
        3  : [b'\x55', b'\xAA', b'\x04', b'\x02', b'\x00', b'\xF9'], #Deshabilitar
        4  : [b'\x55', b'\xAA', b'\x04', b'\x02', b'\x01', b'\xF8'], #Habilitar
        ######### Detección SPO2
        5  : [b'\x55', b'\xAA', b'\x04', b'\x03', b'\x00', b'\xF8'], #Deshabilitar
        6  : [b'\x55', b'\xAA', b'\x04', b'\x03', b'\x01', b'\xF7'], #Habilitar
        ######### Detección Temperatura
        7  : [b'\x55', b'\xAA', b'\x04', b'\x04', b'\x00', b'\xF7'], #Deshabilitar
        8  : [b'\x55', b'\xAA', b'\x04', b'\x04', b'\x01', b'\xF6'], #Habilitar
        ######### Cantidad de derivaciones ECG (3 o 5)
        9  : [b'\x55', b'\xAA', b'\x04', b'\x05', b'\x02', b'\xF4'], #3 Derivadas
        10 : [b'\x55', b'\xAA', b'\x04', b'\x05', b'\x04', b'\xF2'], #5 Derivadas
        ######### Ganancia de ECG
        11 : [b'\x55', b'\xAA', b'\x04', b'\x07', b'\x01', b'\xF3'], #x0.25
        12 : [b'\x55', b'\xAA', b'\x04', b'\x07', b'\x02', b'\xF2'], #x0.5
        13 : [b'\x55', b'\xAA', b'\x04', b'\x07', b'\x03', b'\xF1'], #x1.0
        14 : [b'\x55', b'\xAA', b'\x04', b'\x07', b'\x04', b'\xF0'], #x2.0
        ######### Modo de filtrado ECG
        15 : [b'\x55', b'\xAA', b'\x04', b'\x08', b'\x01', b'\xF2'], #Cirugía (1-25Hz)
        16 : [b'\x55', b'\xAA', b'\x04', b'\x08', b'\x02', b'\xF1'], #Monitor (0.5-75Hz)
        17 : [b'\x55', b'\xAA', b'\x04', b'\x08', b'\x03', b'\xF0'], #Diagnóstico (0.05-100Hz)
        ######### Selección del tipo de paciente
        18 : [b'\x55', b'\xAA', b'\x04', b'\x09', b'\x01', b'\xF1'], #Adulto
        19 : [b'\x55', b'\xAA', b'\x04', b'\x09', b'\x02', b'\xF0'], #Pediátrico
        20 : [b'\x55', b'\xAA', b'\x04', b'\x09', b'\x03', b'\xEF'], #Neonatal
        ######### Presión predeterminada de la manga
        21 : [b'\x55', b'\xAA', b'\x04', b'\x0A', b'\x00', b'\x00'], #CAMBIAR
        ######### Calibrar presión estática NIBP
        22 : [b'\x55', b'\xAA', b'\x04', b'\x0B', b'\x00', b'\xF0'], #Detener calibración
        23 : [b'\x55', b'\xAA', b'\x04', b'\x0B', b'\x01', b'\xEF'], #Empezar calibración
        ######## Configuración de sesgo de presión estática de NIBP
        24 : [b'\x55', b'\xAA', b'\x04', b'\x0C', b'\x00', b'\x00'], #CAMBIAR
        ######## Configuración de sesgo de temperatura
        25 : [b'\x55', b'\xAA', b'\x04', b'\x0D', b'\x00', b'\x00'], #CAMBIAR
        ######### Ganancia de Respiración
        26 : [b'\x55', b'\xAA', b'\x04', b'\x0F', b'\x01', b'\xEB'], #x0.25
        27 : [b'\x55', b'\xAA', b'\x04', b'\x0F', b'\x02', b'\xEA'], #x0.5
        28 : [b'\x55', b'\xAA', b'\x04', b'\x0F', b'\x03', b'\xE9'], #x1.0
        29 : [b'\x55', b'\xAA', b'\x04', b'\x0F', b'\x04', b'\xE8'], #x2.0
        ######### Detección de fugas NIBP
        30 : [b'\x55', b'\xAA', b'\x04', b'\x10', b'\x00', b'\x00'], #CAMBIAR
        ######### Habilitar/Deshabilitar salida de onda de ECG
        31 : [b'\x55', b'\xAA', b'\x04', b'\xFB', b'\x00', b'\x00'], #Deshabilitar
        32 : [b'\x55', b'\xAA', b'\x04', b'\xFB', b'\x01', b'\xFF'], #Habilitar
        ######### Habilitar/Deshabilitar salida de onda de SPO2
        33 : [b'\x55', b'\xAA', b'\x04', b'\xFE', b'\x00', b'\xFD'], #Deshabilitar
        34 : [b'\x55', b'\xAA', b'\x04', b'\xFE', b'\x01', b'\xFC'], #Habilitar
        ######### Habilitar/Deshabilitar salida de onda de Respiración
        35 : [b'\x55', b'\xAA', b'\x04', b'\xFF', b'\x00', b'\xFC'], #Deshabilitar
        36 : [b'\x55', b'\xAA', b'\x04', b'\xFF', b'\x01', b'\xFB']  #Habilitar
    }

    for i in range(0, len(Comandos.get(comando))):
        puerto.write(Comandos.get(comando)[i])
    sleep(0.03)
    print("OK")
