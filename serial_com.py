#!/usr/bin/python 

import os
import sys
import serial
import subprocess
import time
import utils

def serial_port():
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=1)
    return ser;

def write_cmd(cmd):
    out = ''
    ser = serial_port()
    for i in cmd:
        ser.write(i + '\r')
        time.sleep(1)
    while ser.inWaiting() > 0:
        out += ser.read(5)
    ser.close()
    return out
   
def get_build_version():
    cmd = 'git describe'
    path = '~/trackr1/internal/firmware/smart-tag/'
    os.chdir(os.path.expanduser(path))
    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
    version = pipe.read()
    result = version[0:1]+'.'+version[2:3] +'.'+version[4:6]
    return result
    


