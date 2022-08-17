from django.shortcuts import render
from datetime import datetime
from subprocess import Popen, CalledProcessError, PIPE

# Popen dir
RASPBERRY_PATH = './cab/raspberry/'
MEASURE = ['python3', RASPBERRY_PATH+'berry_measurement.py']

current_time = datetime.now()
last_time = datetime.now()
once_flarg = True
measure_pipe = 0

# Create your views here.
def index(request):
    ''' Index view '''
    global last_time
    last_time = datetime.now()
    return render(request,'index.html')

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
    return render(request,'index.html')
