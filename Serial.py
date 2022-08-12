## Fundación Cardiovascular de Colombia
## Proyecto falla cardiaca
## v0.1 11/01/2021 03:00 p.m.

from serial import Serial
from time import sleep
from Comunicacion import Leer
import Metodo

puerto = Serial('/dev/ttyAMA1', 115200)

Dato1=b'\x00'
Dato2=b'\x00'
Dato3=b'\x00'
Dato =b'\x00'

while True:
    Dato1=Dato2
    Dato2=Dato3
    Dato3=Dato

    Dato = puerto.read()
    
    # if((Dato == b'\x02') | (Dato == b'\x03') | (Dato == b'\x04') | (Dato == b'\x05')):
    #     Salida = Leer(Metodo.Convertir(Dato))
    #     print(Salida)

    ############# ECG
    if((Dato1==b'\x55') & (Dato2==b'\xaa') & (Dato3==b'\x09')):
        if(Dato == b'\x02'):
            Salida = Leer(Metodo.Convertir(Dato))
            print(Salida)

    ############# NIBP
    if((Dato1==b'\x55') & (Dato2==b'\xaa') & (Dato3==b'\x08')):
        if(Dato == b'\x03'):
            Salida = Leer(Metodo.Convertir(Dato))
            print(Salida)

    ############# SPO2
    if((Dato1==b'\x55') & (Dato2==b'\xaa') & (Dato3==b'\x06')):
        if(Dato == b'\x04'):
            Salida = Leer(Metodo.Convertir(Dato))
            print(Salida)

    ############# Temperatura
    if((Dato1==b'\x55') & (Dato2==b'\xaa') & (Dato3==b'\x08')):
        if(Dato == b'\x05'):
            Salida = Leer(Metodo.Convertir(Dato))
            print(Salida)

    ###############################################################
    ####################### Formas de ondas #######################
    ###############################################################
    ############# Ondas ECG
    # if((Dato1==b'\x55') & (Dato2==b'\xaa') & (Dato3==b'\x0a')):
    #     if(Dato == b'\x01'):
    #         Salida = Grafica(Metodo.Convertir(Dato))
    ############# Onda SPO2
    # if((Dato1==b'\x55') & (Dato2==b'\xaa') & (Dato3==b'\x04')):
    #     if(Dato == b'\xfe'):
    #         Salida = Grafica(Metodo.Convertir(Dato))
    ############# Onda Respiración
    # if((Dato1==b'\x55') & (Dato2==b'\xaa') & (Dato3==b'\x04')):
    #     if(Dato == b'\xff'):
    #         Salida = Grafica(Metodo.Convertir(Dato))

