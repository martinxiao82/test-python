#!/usr/bin/python
import serial
import time


def serial_port():
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=57600, timeout=1)
    return ser


def write_cmd(cmd):
    out = ''
    ser = serial_port()
    for i in cmd:
        ser.write(i + '\r')
        time.sleep(1)
    while ser.inWaiting() > 0:
        out += ser.read(100)
    ser.close()
    return out
