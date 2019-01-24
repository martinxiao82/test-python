#!/usr/bin/python
import time
import os
import serial_com
import utils
import tdb_auto
import ota


# defines the variant eg. dvt, pvt, evt1, evt2 ..
variant = 'pvt'


# Set current path as SCRIPT_PATH
os.environ['SCRIPT_PATH'] = os.getcwd()
# Steps to trackr and name it TRACKR_PATH
os.chdir('../../../')
os.environ['TRACKR_PATH'] = os.getcwd()
os.environ['nrfjprog_PATH'] = os.environ['TRACKR_PATH'] + \
    '/vendor/nordic/nRF5x-command-line-tools/nrfjprog'
# Steps to smart-tag folder and name it BUILD_PATH
os.chdir('internal/firmware/smart-tag/')
os.environ['BUILD_PATH'] = os.getcwd()
os.environ['FW_PATH'] = os.environ['BUILD_PATH'] + '/build-PVT'
os.environ['TDB_PATH'] = os.environ['TRACKR_PATH'] + \
    '/internal/tools/tdb/build'
os.environ['BT_PATH'] = '/etc/init.d'
os.environ['RESULT_PATH'] = '/home/' + os.environ['USERNAME'] + \
    '/Trackr_Result'
os.environ['DEBUG_PATH'] = os.environ['SCRIPT_PATH'] + '/debug.txt'
os.environ['TEMP_RES_PATH'] = os.environ['SCRIPT_PATH'] + 'temp_result.txt'


while True:
    mac = raw_input('Enter MAC: ')
    if utils.check_MAC(mac) is True:
        print 'Input is a correct MAC adress\n'
        break


# calling the envsetup.sh
utils.env_setup(os.environ['TRACKR_PATH'])
# repo sync and saves output
out = utils.repo_sync(os.environ['BUILD_PATH'])
# asking git for the current version and saves it
version = utils.get_build_version(os.environ['BUILD_PATH'])
# calling the build.sh script
utils.build_and_flash(os.environ['BUILD_PATH'], variant)


# Creates serial port
ser = serial_com.serial_port()
utils.debug('Loading serial connection')

# changes path to where the script is run
os.chdir(os.environ['SCRIPT_PATH'])

if os.path.exists('debug.txt'):
    os.remove('debug.txt')

if os.path.exists('temp_result.txt'):
    os.remove('temp_result.txt')

if ser.isOpen():
    ser.close()
ser.open()
check_ser_port = ser.isOpen()
time.sleep(2)
cmd = ('ets', 'vers')
utils.debug('Checking SW version')
if check_ser_port is True:
    out = serial_com.write_cmd(cmd)
    serial_com.write_cmd('q')
else:
    utils.debug('Serial port is not open')
    ser.open()
    out = serial_com.write_cmd(cmd)
    serial_com.write_cmd('q')

if version in out:
    utils.flash_report(version, 'PASS', 'ETS/VERS the same as Git describe')
    utils.debug('FW version from Git describe: ' + version)
    utils.debug('Current FW version of DUT: ' + out)
else:
    utils.flash_report(version, 'Failed', 'ETS/VERS not the same \
        as Git describe')
    utils.debug('FW version from Git describe: ' + version)
    utils.debug('Current FW version of DUT: ' + out)


####################################

write_MAC_cmd = ('ets', 'PPWR=2,' + mac)
read_MAC_cmd = ('ets', 'PPRE=2')
if check_ser_port is True:
    # Writes the input MAC to DUT
    utils.debug('Writing input MAC to DUT')
    out_write = serial_com.write_cmd(write_MAC_cmd)
    serial_com.write_cmd('q')

    time.sleep(0.05)

    # Resets DUT
    utils.debug('Resetting DUT ...')
    utils.reset(os.environ['nrfjprog_PATH'])
    time.sleep(5)

    # Reads MAC of DUT
    utils.debug('Reading MAC from DUT')
    out_read = serial_com.write_cmd(read_MAC_cmd)
    serial_com.write_cmd('q')

    if mac in out_read:
        utils.debug('Succefully writing input MAC to DUT')
    else:
        utils.debug('Writing MAC to DUT failed')
else:
    utils.debug('Serial port is not open')

    ser.open()

    # Writes the input MAC to DUT
    utils.debug('Writing input MAC to DUT')
    out_write = serial_com.write_cmd(write_MAC_cmd)
    serial_com.write_cmd('q')

    time.sleep(0.05)

    # Resets DUT
    utils.debug('Resetting DUT ...')
    utils.reset(os.environ['nrfjprog_PATH'])
    time.sleep(5)

    # Reads MAC of DUT
    utils.debug('Reading MAC from DUT')
    out_read = serial_com.write_cmd(read_MAC_cmd)
    serial_com.write_cmd('q')

    if mac in out_read:
        utils.debug('Succefully writing input MAC to DUT')
    else:
        utils.debug('Writing MAC to DUT failed')

# Runs tdb_auto.py
tdb_auto.main(mac)

####################################

onboarding_cmd = ('main', 'sonb 1')
change_name_cmd = ('ets', 'PPWR=11,test')
if check_ser_port is True:
    # Puts DUT in onboarding mode
    utils.debug('\nPuts DUT in onboarding mode')
    out = serial_com.write_cmd(onboarding_cmd)
    utils.debug(out)
    serial_com.write_cmd('q')

    time.sleep(0.05)

    # Changes DUT's advertising name to 'SmartTag-test'
    utils.debug('Changes advertising name to SmartTag-test')
    out = serial_com.write_cmd(change_name_cmd)
    time.sleep(0.5)
    utils.debug(out)
    serial_com.write_cmd('q')
else:
    print 'Serial port is not open'
    utils.debug('Serial port is not open')

    ser.open()

    # Puts DUT in onboarding mode
    utils.debug('Puts DUT in onboarding mode')
    out = serial_com.write_cmd(onboarding_cmd)
    utils.debug(out)
    serial_com.write_cmd('q')

    time.sleep(0.05)

    # Changes DUT's advertising name to 'SmartTag-test'
    utils.debug('Changes advertising name to SmartTag-test')
    out = serial_com.write_cmd(change_name_cmd)
    time.sleep(0.5)
    utils.debug(out)
    serial_com.write_cmd('q')

# Resets DUT
utils.reset(os.environ['nrfjprog_PATH'])
time.sleep(5)

# Runs the OTA test
ota.main()

####################################

# Changes path to where the script is run
os.chdir(os.environ['SCRIPT_PATH'])

utils.send_email()
utils.debug('Cleaning up..')
os.remove('temp_result.txt')
os.remove('debug.txt')
exit()
