from django.shortcuts import render
from datetime import datetime
from subprocess import Popen, CalledProcessError, PIPE
from time import sleep

# Popen dir
RASPBERRY_PATH = './cab/raspberry/'
MEASURE = ['python3', RASPBERRY_PATH+'berry_measurement.py']
CURRENT_TOKEN = './cab/raspberry/current_token.txt'

current_time = datetime.now()
last_time = datetime.now()
once_flarg = True
measure_pipe = 0

# Create your views here.
def index(request):
    ''' Index view '''
    global last_time
    last_time = datetime.now()
    return render(request,'index.html', {'current_user':0})

def monitor(request):
    ''' Monitor view '''
    global last_time, current_time, once_flarg, measure_pipe
    current_time = datetime.now() - last_time
    if (current_time.total_seconds() >= 45) or once_flarg:
        last_time = datetime.now()
        if once_flarg:
            once_flarg = False
        try:
            measure_pipe = Popen(MEASURE, stdout=PIPE)
        except CalledProcessError as err:
            print(err)
            measure_pipe.kill()
    print('Time:',current_time.total_seconds())
    user = read_current_user()
    sleep(0.4)
    return render(request,'index.html', {'current_user':user})

def read_current_user():
    f = open(CURRENT_TOKEN,'r')
    token = f.read()
    f.close()
    return int(token)+2
