'''
Fundacion Cardiovascular de Colombia
Proyecto Telsy
Telsy Cab v12.08.2022
Ing. Elmer Rocha Jaime
'''

from datetime import datetime
from berry_io import serial_read, serial_write
from locale import setlocale, LC_ALL
from pytz import timezone
from requests import post as http_post
from serial import Serial

serial = Serial('/dev/ttyAMA1', 115200)
LOCAL = setlocale(LC_ALL, 'es_CO.UTF-8')
MEASUREMENT_TIME = 90 # 90 seconds, 1:30 minutes
URI = 'http://172.30.19.105:8082/api/v1/vitalsignrecords'
AUTH_TOKEN = [
    'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI2IiwiaWF0IjoxNjYwMzQ0MTY2fQ.ao-jJoh8ni_HfHSi99BlgPWJEbQowgjHRd-Nr9CBi68'
]
time_flarg = True
data3 = data2 = data1 = data = 0
ecg_wave = rr = nibp = spo2 = temp = []
index_file = open('current_token.txt','r')
index = int(index_file.read())
index_file.close()

start_time = datetime.now()
try:
    while time_flarg:
        data3 = data2
        data2 = data1
        data1 = data
        data = serial.read()
        if (data3 == b'\x55') and (data2 == b'\xaa'):
            # ECG Wave
            if (data == b'\x01') and time_flarg:
                print('ECG Wave: ', data)
                ecg_wave.append(serial_read(data))
            # ECG Parameters (Respiration Rate)
            elif (data == b'\x02') and time_flarg:
                print('ECG Paramter: ', data)
                rr.append(serial_read(data))
            # NIBP Parameters
            elif (data == b'\x03') and nibp_flarg:
                print('NIBP Paramter: ', data)
                nibp = serial_read(data)
                nibp_end = nibp.split('*')[0]
                if nibp_end != '1' or nibp_end != '9' or nibp_end != '10':
                    time_flarg = False
                nibp.append(nibp)
            # SPO2 Parameters
            elif data == b'\x04':
                print('SPO2 Paramter: ', data)
                spo2.append(serial_read(data))
            # Temperature Parameters
            elif data == b'\x05':
                print('TEMP Paramter: ', data)
                temp.append(serial_read(data))

        current_time = datetime.now() - start_time
        if current_time.total_seconds() >= MEASUREMENT_TIME:
            time_flarg = False
    serial.close()
except KeyboardInterrupt:
    serial.close()
except OSError as err:
    print(err)
    serial.close()

current_date = datetime.now(timezone('America/Bogota')).strftime('%d/%m/%Y')
data_to_send = {
    'RR' : rr[len(rr) - 2],
    'SPO2' : spo2[len(spo2) - 2].split('S')[0],
    'Pulse' : spo2[len(spo2) -2].split('S')[1],
    'Systolic' : nibp[len(nibp)].split('*')[1].split('S')[0],
    'Diastolic' : nibp[len(nibp)].split('*')[1].split('S')[1],
    'MAP' : nibp[len(nibp)].split('*')[1].split('S')[2],
    'Temperature' : temp[len(temp) - 2],
    'Date' : current_date,
    'ECG' : ','.join(ecg_wave)
}
if index <= 20:
    header = {'Authorization': 'Bearer ' + AUTH_TOKEN[index]}
    response = http_post(URI, json=data_to_send, headers=header, timeout=3)
    print(response)

    index_file = open('current_token.txt', 'w')
    index_file.write(str(index+1))
    index_file.close()
else:
    print('No hay más usuarios')