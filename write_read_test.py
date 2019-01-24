#!/usr/bin/python
import serial
import time
import random


def serial_port():
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=57600, timeout=1)
    return ser


def read():
    ser = serial_port()
    return ser.read()


def write_cmd(cmd):
    out = ''
    ser = serial_port()
    for i in cmd:
        ser.write(i + '\r')
        time.sleep(1)
    while ser.inWaiting() > 0:
        out += ser.read()
    ser.close()
    return out


def randomMAC():
    return [0x00, 0x16, 0x3e,
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff)]


def MAC_gen(mac):
    return ':'.join(map(lambda x: "%02x" % x, mac))


def random_uint8_t():
    return ''.join(random.randint(0, 255) for i in range(11))


def report(msg):
    filename = 'result.txt'
    f = open(filename, 'a')
    f.write(msg)
    f.close()


# Creates serial port
ser = serial_port()


if ser.isOpen():
    ser.close()
ser.open()
check_ser_port = ser.isOpen()
time.sleep(2)

if __name__ == '__main__':

    read()
    if check_ser_port is True:
        for i in range(1000):
            mac = MAC_gen(randomMAC())
            print i
            print mac
            report(mac)
            # Writes MAC to DUT
            cmd = ('ets', 'PPWR=2,' + mac)
            out_write = write_cmd(cmd)
            print out_write
            report(out_write)
            time.sleep(0.05)
            write_cmd('q')
            time.sleep(0.05)
            # Reads MAC from DUT
            cmd = ('ets', 'PPRE=2')
            out_read = write_cmd(cmd)
            print out_read
            report(out_read)
            time.sleep(0.05)
            write_cmd('q')
            time.sleep(0.05)
            if mac in out_read:
                res_mac = True
            else:
                res_mac = False
                print 'FAIL'
                break

        if res_mac is True:
            print 'test PASS'
        else:
            print 'test FAIL'


comm = '''
            prod_line_nbr = random_uint8_t()
            print prod_line_nbr
            # Writes prod line nbr to DUT
            cmd = ('ets', 'PPWR=3,' + prod_line_nbr)
            out_write = write_cmd(cmd)
            print out_write
            time.sleep(0.05)
            write_cmd('q')
            time.sleep(0.05)
            # Reads prod line nbr to DUT
            cmd = ('ets', 'PPRE=3')
            out_read = write_cmd(cmd)
            print out_read
            time.sleep(0.05)
            write_cmd('q')
            time.sleep(0.05)
            if prod_line_nbr in out_read:
                res_prod_line_nbr = True
            else:
                res_prod_line_nbr = False

            prod_shift = random_uint8_t()
            print prod_shift
            # Writes prod shift to DUT
            cmd = ('ets', 'PPWR=4,' + prod_shift)
            out_write = write_cmd(cmd)
            print out_write
            time.sleep(0.05)
            write_cmd('q')
            time.sleep(0.05)
            # Reads prod shift to DUT
            cmd = ('ets', 'PPRE=4')
            out_read = write_cmd(cmd)
            print out_read
            time.sleep(0.05)
            write_cmd('q')
            time.sleep(0.05)
            if prod_shift in out_read:
                res_prod_shift = True
            else:
                res_prod_shift = False


if res_prod_line_nbr is False:
    print 'prod_line_nbr FAIL'
else:
    print 'prod_line_nbr PASS'

if res_prod_shift is False:
    print 'prod_shift FAIL'
else:
    print 'prod_shift PASS'
'''
