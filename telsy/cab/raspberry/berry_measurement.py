'''
Fundacion Cardiovascular de Colombia
Proyecto Telsy
Telsy Cab v16.08.2022
Ing. Elmer Rocha Jaime
'''

from datetime import datetime
from berry_io import serial_read, serial_write
from locale import setlocale, LC_ALL
from pytz import timezone
from requests import post as http_post
from serial import Serial
from user_tokens import tokens, server
from time import sleep
from json import dumps

LOCAL = setlocale(LC_ALL, 'es_CO.UTF-8')
TOKEN_PATH = './cab/raspberry/current_token.txt'
DATE_PATH = './cab/raspberry/current_date.txt'
MEASUREMENT_TIME = 90 # 90 seconds, 1:30 minutes
URI = server()
AUTH_TOKEN = tokens()
serial = Serial('/dev/ttyACM0', 115200)
nibp_once = True
time_flarg = True
data3 = data2 = data1 = data = 0,0,0,0
ecg_wave = []
rr = []
nibp = []
spo2 = []
temp = []
index_file = open(TOKEN_PATH, 'r')
date_txt = open(DATE_PATH, 'r')
index = int(index_file.read())
date_file = date_txt.read()
index_file.close()
date_txt.close()

current_date = datetime.now(timezone('America/Bogota')).strftime('%d/%m/%Y')
if date_file != current_date:
    date_file = current_date
    date_txt = open(DATE_PATH, 'w')
    index_file = open(TOKEN_PATH, 'w')
    date_txt.write(current_date)
    index_file.write('0')
    date_txt.close()
    index_file.close()
    sleep(0.2)
if date_file == current_date:
    if index < 20:
        start_time = datetime.now()
        try:
            while time_flarg:
                if nibp_once:
                    nibp_once = False
                    serial_write(4)
                    sleep(0.1)
                data3 = data2
                data2 = data1
                data1 = data
                data = serial.read()
                if (data3 == b'\x55') and (data2 == b'\xaa'):
                    # ECG Wave
                    if (data == b'\x01') and time_flarg:
                        ecg_ = serial_read(data)
                        # print('ECG Wave: ', ecg_)
                        ecg_wave.append(ecg_)
                    # ECG Parameters (Respiration Rate)
                    elif (data == b'\x02') and time_flarg:
                        ecgw_ = serial_read(data)
                        print('ECG Parameter: ', ecgw_)
                        rr.append(ecgw_)
                    # NIBP Parameters
                    elif (data == b'\x03'):
                        nibp_1 = serial_read(data)
                        print('NIBP Parameter: ', nibp_1)
                        nibp_end = nibp_1.split('*')[0]
                        if nibp_end == '0':
                            time_flarg = False
                        nibp.append(nibp_1)
                    # SPO2 Parameters
                    elif data == b'\x04':
                        spo2_ = serial_read(data)
                        print('SPO2 Parameter: ', spo2_)
                        spo2.append(spo2_)
                    # Temperature Parameters
                    elif data == b'\x05':
                        temp_ = serial_read(data)
                        print('TEMP Parameter: ', temp_)
                        temp.append(temp_)

                current_time = datetime.now() - start_time
                if current_time.total_seconds() >= MEASUREMENT_TIME:
                    time_flarg = False
            serial_write(3)
            sleep(0.1)
            serial.close()
        except KeyboardInterrupt:
            serial_write(3)
            sleep(0.1)
            serial.close()
        except OSError as err:
            print(err)
            serial_write(3)
            sleep(0.1)
            serial.close()
        serial.close()
        sleep(0.1)

        print('ECG Wave:',len(ecg_wave),'RR len:',len(rr),'SPO2 len:',len(spo2),'NIBP len:',len(nibp),'TEMP len:',len(temp))
        data_to_send = {
            'patient': {'id': index+2},
            'RR' : rr[len(rr) - 2],
            'SPO2' : spo2[len(spo2) - 2].split('S')[0],
            'Pulse' : spo2[len(spo2) -2].split('S')[1],
            'Systolic' : nibp[len(nibp) - 1].split('*')[1].split('S')[0],
            'Diastolic' : nibp[len(nibp) - 1].split('*')[1].split('S')[1],
            'MAP' : nibp[len(nibp) - 1].split('*')[1].split('S')[2],
            'Temperature' : temp[len(temp) - 2],
            'Date' : current_date,
            'ECG' : ','.join(ecg_wave)
        }

        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + AUTH_TOKEN[index]}
        response = http_post(URI, data=dumps(data_to_send), headers=header, timeout=5)
        print(response)

        index_file = open(TOKEN_PATH, 'w')
        index_file.write(str(index+1))
        index_file.close()
    else:
        print('No hay más usuarios')
