'''
Fundacion Cardiovascular de Colombia
Proyecto Telsy
Telsy Cab v12.08.2022
Ing. Elmer Rocha Jaime
'''

from serial import Serial
import berry_decoder

serial = Serial('/dev/ttyAMA1', 115200)


def get_length(parameter):
    ''' Returns the number of bytes to read depending on the type of data '''
    parameters = {
        0x01 : 7, ## 01 ECG Wave
        0x02 : 5, ## 02 ECG Param
        0x03 : 5, ## 03 NIBP Param
        0x04 : 3, ## 04 SPO2 Param
        0x05 : 3, ## 05 TEMP Param
        0xFE : 1, ## FE SPO2 Wave
        0xFF : 1  ## FF RESP Wave
    }
    return parameters.get(parameter)


def get_int(bytes):
    ''' Converts the data in bytes to integer '''
    return int.from_bytes(bytes, byteorder='big', signed=False)


def serial_read(serial_data):
    ''' Read the serial data sent by the card '''
    data = get_int(serial_data)
    data_length = get_length(data)
    buffer = []
    response = ''
    for _ in range(0, data_length):
        buffer.append(get_int(serial.read()))

    if data == 0x01:
        response = berry_decoder.ecg_wave(buffer)
    elif data == 0x02:
        response = berry_decoder.ecg_parameters(buffer)
    elif data == 0x03:
        response = berry_decoder.nibp(buffer)
    elif data == 0x04:
        response = berry_decoder.spo2(buffer)
    elif data == 0x05:
        response = berry_decoder.temperature(buffer)
    elif data == 0xFE:
        response = berry_decoder.spo2_wave(buffer)
    elif data == 0XFF:
        response = berry_decoder.respiration_wave(buffer)

    return response