## Fundación Cardiovascular de Colombia
## Proyecto falla cardiaca
## v0.1 11/01/2021 03:00 p.m.

from serial import Serial
from time import sleep
from Comunicacion import Leer, Escribir
import Metodo

puerto = Serial('/dev/ttyAMA1', 115200)

Dato1=b'\x00'
Dato2=b'\x00'
Dato3=b'\x00'
Dato =b'\x00'

sleep(1)
Escribir(4)
sleep(1)

while True:
    Dato1=Dato2
    Dato2=Dato3
    Dato3=Dato

    Dato = puerto.read()

    ############# NIBP
    if((Dato1==b'\x55') & (Dato2==b'\xaa') & (Dato3==b'\x08')):
        if(Dato == b'\x03'):
            Salida = Leer(Metodo.Convertir(Dato))
            print(Salida)

