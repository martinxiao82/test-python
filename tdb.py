#!/usr/bin/python
import subprocess
import os
import utils
import traceback


# Function that starts the TDB server in a separate terminal
def start_tdb_server(bt_path, tdb_path):
    # Restarts the BT service
    os.chdir(bt_path)
    subprocess.check_call('sudo ./bluetooth stop', shell=True)
    subprocess.check_call('sudo ./bluetooth start', shell=True)

    # Changes to TDB path
    os.chdir(tdb_path)

    # Starts the TDB server
    start_server_cmd = 'gnome-terminal -e \'./tdb server\''
    print '\nStarting tdb server\n'
    p = subprocess.Popen(start_server_cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        utils.debug(err)
    utils.debug(out)
    return out


def start_scan():
    CMD = './tdb enable-scan'
    utils.debug('Initiating scan')
    proc = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    (out, err) = proc.communicate()
    if err:
        utils.debug(err)
        return 'ERROR'
    else:
        utils.debug(out)
        return out


def ble_param(MAC, param):
    CMD = './tdb ble-param ' + MAC + ' ' + param
    utils.debug('Setting BLE Param: ' + param)
    proc = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    (out, err) = proc.communicate()
    if err:
        utils.debug(err)
        return 'ERROR'
    else:
        utils.debug(out)
        return out


def stop_scan():
    CMD = './tdb disable-scan'
    utils.debug('Stopping scan')
    proc = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    (out, err) = proc.communicate()
    if err:
        utils.debug(err)
        return 'ERROR'
    else:
        utils.debug(out)
        return out


def connect(MAC):
    CMD = './tdb connect ' + MAC
    utils.debug('Connecting to: ' + MAC)
    proc = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    (out, err) = proc.communicate()
    if err:
        utils.debug(err)
        return 'ERROR'
    else:
        utils.debug(out)
        return out


def disconnect(MAC):
    CMD = './tdb disconnect ' + MAC
    utils.debug('Disconnected from: ' + MAC)
    result = subprocess.check_call(CMD, shell=True)
    utils.debug(result)


def ping(MAC, arg):
    CMD = './tdb ping ' + MAC + ' ' + arg
    utils.debug('Ping!')
    proc = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    (out, err) = proc.communicate()
    if err:
        utils.debug(err)
        return 'ERROR'
    else:
        utils.debug(out)
        return out


def onboard_start(MAC):
    CMD = './tdb onboard-start ' + MAC
    utils.debug('Onboard start')
    proc = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    (out, err) = proc.communicate()
    if err:
        utils.debug(err)
        return 'ERROR'
    else:
        utils.debug(out)
        return out


def onboard_confirm(MAC):
    CMD = './tdb onboard-confirm ' + MAC
    utils.debug('Onboard confirm')
    proc = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    (out, err) = proc.communicate()
    if err:
        utils.debug(err)
        return 'ERROR'
    else:
        utils.debug(out)
        return out


def onboard_cancel(MAC):
    CMD = './tdb onboard-cancel ' + MAC
    utils.debug('Off boarding')
    proc = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    (out, err) = proc.communicate()
    if err:
        utils.debug(err)
        return 'ERROR'
    else:
        utils.debug(out)
        return out


def container_settings_ON(MAC, rssi):
    CMD = './tdb container-settings ' + MAC + ' 2 0 0 -' + rssi
    utils.debug('Enabling container with rssi: ' + rssi)
    result = subprocess.check_call(CMD, shell=True)
    utils.debug(result)


# Usage: container-item TAG_MAC SLOT TAGLET_MAC Status
# Slot is the slot talgets is added, status is 0 for delete 1 for add.
def container_item(MAC, SLOT, TAGLET_MAC, status):
    CMD = './tdb container-item ' + MAC + ' ' + SLOT + ' ' + TAGLET_MAC + \
        ' ' + status
    print 'Container status for: ' + MAC
    result = subprocess.check_call(CMD, shell=True)
    print result


def container_item_version(MAC):
    CMD = './tdb container-item-version ' + MAC
    print 'Connected item SW revision for ' + MAC
    result = subprocess.check_call(CMD, shell=True)
    print result


def container_confirm(MAC):
    CMD = './tdb container-confirm ' + MAC
    print 'Confirmed!'
    result = subprocess.check_call(CMD, shell=True)
    print result


# Function that changes container item OTA lock status
# Flag is 0 for unlocking OTA and 1 for locking OTA
# item_ID = -1 when item_MAC should be used
def container_item_lock(MAC, item_ID, flag, item_MAC):
    CMD = './tdb container-item-lock ' + MAC + ' ' + item_ID + ' ' + flag + \
        ' ' + item_MAC
    print 'Changing container item OTA lock status'
    result = subprocess.check_call(CMD, shell=True)
    print result


def container_status(MAC):
    CMD = './tdb status ' + MAC
    print 'Acquiring container status for: ' + MAC
    result = subprocess.check_call(CMD, shell=True)
    print result


def ring_start(MAC):
    CMD = './tdb ring ' + MAC + ' 1 1'
    utils.debug('Start ringing: ' + MAC)
    proc = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    (out, err) = proc.communicate()
    if err:
        utils.debug(err)
        return 'ERROR'
    else:
        utils.debug(out)
        return out


def ring_stop(MAC):
    CMD = './tdb ring ' + MAC + ' 1 0'
    utils.debug('Stop ringing: ' + MAC)
    proc = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    (out, err) = proc.communicate()
    if err:
        utils.debug(err)
        return 'ERROR'
    else:
        utils.debug(out)
        return out


def factory_reset(MAC, timeout):
    CMD = './tdb factory-reset ' + MAC + ' ' + timeout
    utils.debug('Reset initiated you have ' + timeout +
                ' seconds to press buttons')
    result = subprocess.check_call(CMD, shell=True)
    print result


def log_rssi(MAC):
    CMD = './tdb log-rssi ' + MAC
    print 'Requesting a constant stream of container statuses for ' + MAC
    result = subprocess.check_call(CMD, shell=True)
    print result


def scan_instant(MAC, duration_ms):
    CMD = './tdb scan-instant ' + MAC + ' ' + duration_ms
    print 'Running instant scan for ' + MAC + 'during ' + duration_ms + ' ms'
    result = subprocess.check_call(CMD, shell=True)
    print result


def scan_periodic_start(MAC, duration_ms, interval_ms):
    CMD = './tdb scan-periodic-start ' + MAC + ' ' + duration_ms + \
        ' ' + interval_ms
    print 'Starting periodic scan for ' + MAC + ' for ' + duration_ms + \
        ' ms, repeating ' + interval_ms + ' ms'
    result = subprocess.check_call(CMD, shell=True)
    print result


def scan_periodic_stop(MAC):
    CMD = './tdb scan-periodic-stop ' + MAC
    print 'Stopping periodic scan for ' + MAC
    result = subprocess.check_call(CMD, shell=True)
    print result


def scan_accelparams_define(MAC, duration_ms, movement_scan_enable,
                            movement_filter_ms, resting_scan_enable,
                            resting_filter_ms):
    CMD = './tdb scan-accelparams-define ' + MAC + ' ' + duration_ms + ' ' + \
        movement_scan_enable + ' ' + movement_filter_ms + ' ' + \
        resting_scan_enable + ' ' + resting_filter_ms
    print 'Define accelerometer scan parameters for ' + MAC
    result = subprocess.check_call(CMD, shell=True)
    print result


# Function that kills the TDB server
def kill_tdb_server():
    utils.debug('Killing tdb server')
    try:
        out = subprocess.check_call('sudo killall -9 tdb', shell=True)
    except (subprocess.CalledProcessError) as err:
        traceback.format_exc()
        utils.debug(str(err))
        return err
    else:
        utils.debug(str(out))
        return out
