from serial import Serial
from time import sleep
from Comunicacion import Leer, Escribir
import Metodo

puerto = Serial('/dev/ttyAMA1', 115200)

Escribir(4)



