#!/usr/bin/python
from bluepy.btle import Scanner
import tdb
import os
import traceback
import subprocess
import time

# Parameters
rssi = '60'
param = '6 6 0 3200 23'
command = ''
timeout = '60'
ping_cmd = 'Ping!'
tdb_is_killed = False

_USERNAME = os.getenv("SUDO_USER") or os.getenv("USER")
os.environ['TDB_PATH'] = os.path.expanduser('~' + _USERNAME) + \
    '/trackr1/internal/tools/tdb/build'
os.environ['SCRIPT_PATH'] = os.path.expanduser('~' + _USERNAME) + \
    '/trackr1/internal/tools/test'
os.environ['DEBUG_TXT_PATH'] = os.path.join(os.environ['SCRIPT_PATH'],
                                            'debug.txt')
os.environ['BT_PATH'] = '/etc/init.d'


# Function that scans for nearby Smarttags
# and allows user to choose the tag from the scanning list
def scan_tags():
    scanner = Scanner()
    scan_time = 5.0
    print 'Scanning SmartTag devices for ' + str(scan_time) + ' sec'
    devices = scanner.scan(scan_time)
    print("Results...")
    tag_set = []
    for dev in devices:
        # print "Device: %s, RSSI=%d dB" % (dev.addr, dev.rssi)
        for (adtype, desc, value) in dev.getScanData():
            # print("  %s = %s" % (desc, value))
            if 'SmartTag' in value:
                tag = dev.addr + ' ' + value
                tag_set.append(tag)

    tag_set_dict = dict()
    for k in range(len(tag_set)):
        tag_set_dict[k + 1] = tag_set.pop()

    for key in sorted(tag_set_dict):
        print '%s: %s' % (key, tag_set_dict[key])

    ans = raw_input('\nCan you find your tag from the list? (Y/N): ')
    if ans == 'Y' or ans == 'y':
        key = raw_input('Choose your tag nbr: ')
        print '\n'
        while not(key.isdigit()):
            key = raw_input('Please insert a number: ')
            print '\n'
        else:
            MAC = tag_set_dict[int(key)].split(' ')[0]

            print ('Your tag have MAC adress: ' + MAC)
            return MAC
    else:
        print 'Continue scanning ...'
        return scan_tags()


# adding colors for fun
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# parsing inputs into commands
def cmd_parser(input):
    if input == '1':
        return tdb.start_tdb_server(os.environ['BT_PATH'],
                                    os.environ['TDB_PATH'])

    elif input == '2':
        return tdb.start_scan()

    elif input == '3':
        return tdb.stop_scan()

    elif input == '4':
        return tdb.connect(MAC)

    elif input == '12':
        return tdb.ble_param(MAC, param)

    elif input == '5':
        return tdb.disconnect(MAC)

    elif input == '6':
        return tdb.onboard_start(MAC)

    elif input == '7':
        return tdb.onboard_confirm(MAC)

    elif input == '8':
        return tdb.onboard_cancel(MAC)

    elif input == '9':
        return tdb.container_settings_ON(MAC, rssi)

    elif input == '10':
        return tdb.container_confirm(MAC)

    elif input == '11':
        return tdb.factory_reset(MAC, timeout)

    elif input == '13':
        return tdb.ping(MAC, ping_cmd)

    elif input == '14':
        return tdb.ring_start(MAC)

    elif input == '15':
        return tdb.ring_stop(MAC)

    elif input == '16':
        global tdb_is_killed
        if tdb_is_killed is False:
            out = tdb.kill_tdb_server()
            if out == 0:
                tdb_is_killed = True
            else:
                tdb_is_killed = False
        else:
            print 'tdb is already terminated'

    elif input == 'q':
        if tdb_is_killed is False:
            tdb.kill_tdb_server()
            tdb_is_killed = True
        if os.path.exists(os.environ['DEBUG_TXT_PATH']):
            os.remove(os.environ['DEBUG_TXT_PATH'])
        print 'Bye bye!'

    else:
        if 'M' in input:
            input = input.replace('M', MAC)

        print '\nAre you sure that you want to run following command? (Y/N):'
        ans = raw_input(input + '\n')
        if ans == 'Y' or ans == 'y':
            try:
                print '\nRunning following command: '
                print input
                print ''
                result = subprocess.check_call(input, shell=True)
                print result
            except (subprocess.CalledProcessError) as detail:
                traceback.format_exc()
                print detail
        else:
            print 'Try again'


# A fun help menu
def help_menu():
    print 30 * '-', 'menu', 30 * '-'
    print ''
    print 15 * ' ', bcolors.WARNING + 'FOLLOWING COMMANDS ARE AVAILABLE:' \
        + bcolors.ENDC
    print ''
    print 13 * ' ', bcolors.OKGREEN + '1.start_server  2.scan  3.stop_scan' \
        '  4.connect' + bcolors.ENDC
    print ''
    print 3 * ' ', bcolors.OKGREEN + '5.disconnect  6.onboard_start' \
        '  7.onboard_confirm  8.onboard_cancel' + bcolors.ENDC
    print ''
    print 5 * ' ', bcolors.OKGREEN + '9.container_settings_ON' \
        '  10.container_confirm  11.factory_reset' + bcolors.ENDC
    print ''
    print 3 * ' ', bcolors.OKGREEN + '12.ble_param  13.ping  14.ring_start' \
        '  15.ring_stop  16.kill  q.quit' + bcolors.ENDC
    print ''
    print bcolors.WARNING + '** Please add fri text if you want to ' \
        'run anything else than these quick options **' + bcolors.ENDC
    print 13 * ' ', bcolors.WARNING + '** You can insert M instead of MAC ' \
        'in your command **' + bcolors.ENDC
    print ''
    print 67 * '-'


# loop waiting for input until quit is pressed.
if __name__ == '__main__':
    # Scans for user's MAC
    MAC = scan_tags()

    # Starts the TDB server
    tdb.start_tdb_server(os.environ['BT_PATH'], os.environ['TDB_PATH'])
    time.sleep(1)

    while command != 'q':
        try:
            help_menu()
            command = raw_input('Enter command: ')
            cmd_parser(command)
        except (TypeError, subprocess.CalledProcessError, NameError) as detail:
            traceback.format_exc()
            print detail
        except KeyboardInterrupt:
            print '\nAborted by user\n'
            cmd_parser('q')
            break
