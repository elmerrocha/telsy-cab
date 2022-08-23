'''
Fundacion Cardiovascular de Colombia
Proyecto Telsy
Telsy Cab v23.08.2022
Ing. Elmer Rocha Jaime
'''

from serial import Serial
import berry_decoder

serial = Serial('/dev/ttyACM0', 115200)


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


def serial_write(command):
    ''' Sends configuration data to the module via serial '''

    commands = {
        1 : [0x55, 0xAA, 0x04, 0x01, 0x00, 0xFA],  # Disable ECG parameter Output
        2 : [0x55, 0xAA, 0x04, 0x01, 0x01, 0xF9],  # Enable ECG parameter Output
        3 : [0x55, 0xAA, 0x04, 0x02, 0x00, 0xF9],  # Stop current NIBP Detection
        4 : [0x55, 0xAA, 0x04, 0x02, 0x01, 0xF8],  # Start NIBP Detection
        5 : [0x55, 0xAA, 0x04, 0x03, 0x00, 0xF8],  # Disable SPO2 parameter Output
        6 : [0x55, 0xAA, 0x04, 0x03, 0x01, 0xF7],  # Enable SPO2 parameter Output
        7 : [0x55, 0xAA, 0x04, 0x04, 0x00, 0xF7],  # Disable TEMP parameter Output
        8 : [0x55, 0xAA, 0x04, 0x04, 0x01, 0xF6],  # Enable TEMP parameter Output
        9 : [0x55, 0xAA, 0x04, 0x05, 0x02, 0xF4],  # Lead3 mode
        10 : [0x55, 0xAA, 0x04, 0x05, 0x03, 0xF2],  # Lead5 mode *
        11 : [0x55, 0xAA, 0x04, 0x07, 0x01, 0xF3],  # ECG Wave Gain x0.25
        12 : [0x55, 0xAA, 0x04, 0x07, 0x02, 0xF2],  # ECG Wave Gain x0.5
        13 : [0x55, 0xAA, 0x04, 0x07, 0x03, 0xF1],  # ECG Wave Gain x1
        14 : [0x55, 0xAA, 0x04, 0x07, 0x04, 0xF0],  # ECG Wave Gain x2
        15 : [0x55, 0xAA, 0x04, 0x08, 0x01, 0xF2],  # ECG Filter operation Mode
        16 : [0x55, 0xAA, 0x04, 0x08, 0x02, 0xF1],  # ECG Filter monitor Mode *
        17 : [0x55, 0xAA, 0x04, 0x08, 0x03, 0xF0],  # ECG Filter diagnose Mode
        18 : [0x55, 0xAA, 0x04, 0x09, 0x01, 0xF1],  # NIBP Patient adult Mode *
        19 : [0x55, 0xAA, 0x04, 0x09, 0x02, 0xF0],  # NIBP Patient child Mode
        20 : [0x55, 0xAA, 0x04, 0x09, 0x03, 0xEF],  # NIBP Patient neonate Mode
        21 : [0x55, 0xAA, 0x04, 0x0F, 0x01, 0xEB],  # RESP Wave Gain x0.25
        22 : [0x55, 0xAA, 0x04, 0x0F, 0x02, 0xEA],  # RESP Wave Gain x0.5
        23 : [0x55, 0xAA, 0x04, 0x0F, 0x03, 0xE9],  # RESP Wave Gain x1 *
        24 : [0x55, 0xAA, 0x04, 0x0F, 0x04, 0xE8],  # RESP Wave Gain x2
        25 : [0x55, 0xAA, 0x04, 0xFB, 0x00, 0x00],  # Disable ECG wave output
        26 : [0x55, 0xAA, 0x04, 0xFB, 0x01, 0xFF],  # Enable ECG wave output
        27 : [0x55, 0xAA, 0x04, 0xFE, 0x00, 0xFD],  # Disable SPO2 wave output
        28 : [0x55, 0xAA, 0x04, 0xFE, 0x01, 0xFC],  # Enable SPO2 wave output
        29 : [0x55, 0xAA, 0x04, 0xFF, 0x00, 0xFC],  # Disable RESP wave output
        30 : [0x55, 0xAA, 0x04, 0xFF, 0x01, 0xFB]  # Enable RESP wave output
        # * Default mode
    }
    for cmd in range(0, len(commands.get(command))):
        serial.write(commands.get(command)[cmd].to_bytes(1, 'big'))
