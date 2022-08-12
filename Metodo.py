## Fundación Cardiovascular de Colombia
## Proyecto falla cardiaca

def Longitud(Tamanio):
    """ Devuelve la cantidad de bytes para la lectura dependiendo del tipo de dato. """

    Longitud = {
        0x01 : 7, ## 01 ECG Wave
        0x02 : 5, ## 02 ECG Param
        0x03 : 5, ## 03 NIBP Param
        0x04 : 3, ## 04 SPO2 Param
        0x05 : 3, ## 05 TEMP Param
        0xFE : 1, ## FE SPO2 Wave
        0xFF : 1  ## FF RESP Wave
    }

    return Longitud.get(Tamanio)

def Parametro(Elemento):
    """ Devuelve el string del tipo de variable correspondiente al dato ingresado """
    Parametros = {
        0x01 : "Onda ECG",
        0x02 : "Parámetros ECG",
        0x03 : "Parámetros NIBP",
        0x04 : "Parámetros SPO2",
        0x05 : "Parámetros Temperatura",
        0xFE : "Onda SPO2",
        0xFF : "Onda Respiración"                                
    }
    return Parametros.get(Elemento)

def Convertir(Dato):
    """ Convierte a entero el dato en bytes """
    return int.from_bytes(Dato, byteorder='big')

def ECG(Dato):
    """ Devuelve el valor de la frecuencia cardiaca y respiratoria """
    #Byte1 = Dato[0] 
    #Byte2 = Dato[1] 
    #Byte3 = Dato[2] 
    #Byte4 = Dato[3] 
    #Byte5 = Dato[4]

    #0x01 : 0000 0001
    #0x02 : 0000 0010
    #0x0C : 0000 1100
    #0x30 : 0011 0000
    #0xC0 : 1100 0000

    # IntensidadECG = Dato[0] & 0x01
    # EstadoDerivada = (Dato[0] & 0x02) >> 1
    # GananciaECG = (Dato[0] & 0x0C) >> 2
    # ModoFiltroECG = (Dato[0] & 0x30) >> 4
    # ModoDerivadas = (Dato[0] & 0xC0) >> 6

    HR = Dato[1]
    RR = Dato[2]

    if(HR==0 | RR==0):
        return["---","---"]
    else:
        return [HR,RR]

def NIBP(Dato):
    """ Devuelve la presión sístole, díastole y media """
    #Byte1 = Dato[0] 
    #Byte2 = Dato[1] 
    #Byte3 = Dato[2] 
    #Byte4 = Dato[3] 
    #Byte5 = Dato[4]

    #0x03 : 0000 0011
    #0x3C : 0011 1100

    # TipoPaciente = Dato[0] & 0x03
    # Estado = (Dato[0] & 0x3C) >> 2
    P_Manga = Dato[1] * 2

    Sistole  = Dato[2]
    Diastole = Dato[4]
    Media    = Dato[3]

    if(Sistole==0 | Diastole==0 | Media==0):
        return [P_Manga,"---","---","---"]
    else:
        return [P_Manga,Sistole,Diastole,Media]

def SPO2(Dato):
    """ Devuelve los valores del pulso cardiaco y SPO2 """
    #Byte1 = Dato[0] 
    #Byte2 = Dato[1] 
    #Byte3 = Dato[2]

    #0x07 : 0000 0111

    # Estado = Dato[0] & 0x07

    spo2 = Dato[1]
    Pulso = Dato[2]

    if((spo2 == 127) | (Pulso == 255)):
        return ["---","---"]
    else:
        return [spo2,Pulso]


def Temperatura(Dato):#No vamos a usarla en monitor paciente para falla cardiaca
    """ Devuelve el valor de la temperatura """
    #Byte1 = Dato[0]
    #Byte2 = Dato[1]
    #Byte3 = Dato[2]

    #0x01 : 0000 0001

    #Estado = Dato[0] & 0x01

    Temp = Dato[1] + (Dato[2]/10)

    if (Temp == 0):
        return ["---"]
    else:
        return [Temp]
