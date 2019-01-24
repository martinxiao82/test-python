#!/usr/bin/python
import os
import subprocess
import traceback
import time
import tdb
import utils


# defines the parameters for running TDB
ble_param = '6 6 0 3200 25'  # high connection param
rssi = 60
ping_msg = 'Ping!'
retries = 3


def main(mac):
    cont = False
    next_ring = False
    utils.debug('\n\n******TDB TEST******\n')

    # Starts TDB server
    utils.debug('Starting TDB server')
    tdb.start_tdb_server(os.environ['BT_PATH'],
                         os.environ['TDB_PATH'])
    time.sleep(0.05)

    try:
        # Run connect first as a workaround to make tdb work
        tdb.connect(mac)
        time.sleep(0.05)

        tdb_res = 0
        fail_str = ''
        pass_str = ''

        out_scan = tdb.start_scan()
        time.sleep(2)
        if 'ERROR' in out_scan:
            next_scan = False
            utils.debug('Error while enabling scan')
            fail_str += '\nenable-scan error'
        else:
            if ('set scan enabled' in out_scan):
                next_scan = True
                utils.debug('successfully enabled scan')
                tdb_res += 1
                pass_str += '\nenable-scan pass'
            else:
                next_scan = False
                utils.debug('failed to enable scan')
                fail_str += '\nenable-scan failed'

        if next_scan is True:
            out_conn = tdb.connect(mac)
            time.sleep(0.05)
            if 'ERROR' in out_conn:
                utils.debug('Error happens when connecting to tdb')
                next_conn = False
            else:
                if ('error' in out_conn) or ('connection to tdb server \
                                             failed' in out_conn):
                    utils.debug('connection to tdb server failed')
                    next_conn = False
                elif ('connection open!' in out_conn):
                    utils.debug('successfully connected to tdb server')
                    next_conn = True
                    tdb_res += 1
                    pass_str += '\ntdb connect pass'

        if next_conn is False:
            for i in range(retries):
                try:
                    utils.debug('Loop: ' + str(i + 1))
                    utils.debug('Resetting DUT ...')
                    utils.reset(os.environ['nrfjprog_PATH'])
                    time.sleep(5)
                    tdb.start_tdb_server(os.environ['BT_PATH'],
                                         os.environ['TDB_PATH'])
                    tdb.connect(mac)
                    time.sleep(0.05)
                    tdb.start_scan()
                    time.sleep(2)
                    out_conn = tdb.connect(mac)
                    time.sleep(0.05)
                    if ('connection open!' in out_conn):
                        utils.debug('successfully connected to tdb server \
                            after ' + str(i + 1) + 'retries')
                        next_conn = True
                        tdb_res += 1
                        pass_str += '\ntdb connect pass'
                        break
                except (subprocess.CalledProcessError) as detail:
                    traceback.format_exc()
                    print detail
                    utils.debug(str(detail))
                    if i < 2:
                        continue
                    else:
                        raise

        if next_conn is False:
            utils.debug('Failed to connect to tdb server after ' +
                        str(retries) + ' retries')
            fail_str += '\ntdb connect failed'
        else:
            out_stop_scan = tdb.stop_scan()
            time.sleep(0.05)
            if 'ERROR' in out_stop_scan:
                utils.debug('Error while disabling scan')
                fail_str += '\ntdb disable-scan failed'
            else:
                tdb_res += 1
                pass_str += '\ntdb disable-scan pass'

            out_onb_start = tdb.onboard_start(mac)
            time.sleep(0.05)
            if 'ERROR' in out_onb_start:
                utils.debug('onboard-start error')
                cont = False
                fail_str += '\ntdb onboard-start error'
            else:
                if 'received response' in out_onb_start:
                    cont = True
                    utils.debug('onboard start OK')
                    tdb_res += 1
                    pass_str += '\ntdb onboard-start pass'
                else:
                    cont = False
                    utils.debug('Failed to start onboarding')
                    fail_str += '\nonboard-start failed'

        if cont is True:
            out_onb_conf = tdb.onboard_confirm(mac)
            time.sleep(0.05)
            if 'ERROR' in out_onb_conf:
                cont = False
                utils.debug('onboard confirm error')
                fail_str += '\ntdb onboard-confirm error'
            else:
                if ('Tag device id' in out_onb_conf):
                    cont = True
                    utils.debug('onboard confirm OK')
                    tdb_res += 1
                    pass_str += '\ntdb onboard-confirm pass'
                else:
                    cont = False
                    utils.debug('Failed to onboard confirm')
                    fail_str += '\ntdb onboard-confirm failed'

        if cont is True:
            out_onb_cancel = tdb.onboard_cancel(mac)
            time.sleep(0.05)
            if 'ERROR' in out_onb_cancel:
                cont = False
                utils.debug('Off onboarding error')
                fail_str += '\ntdb onboard-cancel error'
            else:
                if ('received response' in out_onb_cancel):
                    cont = True
                    utils.debug('off boarding OK')
                    tdb_res += 1
                    pass_str += '\ntdb onboard-cancel pass'
                else:
                    cont = False
                    utils.debug('off boarding failed')
                    fail_str += '\ntdb onboard-cancel failed'

        if next_conn is True:
            out_ble_param = tdb.ble_param(mac, ble_param)
            time.sleep(0.05)
            if 'ERROR' in out_ble_param:
                utils.debug('Error when setting ble param')
                fail_str += '\ntdb ble-param error'
            else:
                if ('error code: 0'in out_ble_param):
                    utils.debug('successfully setting ble param')
                    tdb_res += 1
                    pass_str += '\ntdb ble-param pass'
                else:
                    utils.debug('failed to set ble_param')
                    fail_str += '\ntdb ble-param failed'

        if next_conn is True:
            out_ping = tdb.ping(mac, ping_msg)
            time.sleep(0.05)
            if 'ERROR' in out_ping:
                utils.debug('Error when pinging')
                fail_str += '\ntdb ping error'
            else:
                if ('received pong msg="Ping!"' in out_ping):
                    utils.debug('ping OK')
                    tdb_res += 1
                    pass_str += '\ntdb ping pass'
                else:
                    utils.debug('ping failed')
                    fail_str += '\ntdb ping failed'

        if next_conn is True:
            out_ring = tdb.ring_start(mac)
            time.sleep(0.05)
            if 'ERROR' in out_ring:
                utils.debug('Error when ringing')
                next_ring = False
                fail_str += '\ntdb ring error'
            else:
                if ('Ring indication: error code: 0' in out_ring):
                    utils.debug('Ring OK')
                    next_ring = True
                    tdb_res += 1
                    pass_str += '\ntdb ring pass'
                else:
                    utils.debug('Ring failed')
                    next_ring = False
                    fail_str += '\ntdb ring failed'

        if next_ring is True:
            out_ring_stop = tdb.ring_stop(mac)
            time.sleep(0.05)
            if 'ERROR' in out_ring_stop:
                utils.debug('ring-stop error')
                fail_str += '\ntdb ring-stop error'
            else:
                if ('Ring indication: error code: 0' in out_ring_stop):
                    utils.debug('ring-stop OK')
                    tdb_res += 1
                    pass_str += '\ntdb ring-stop pass'
                else:
                    utils.debug('failed to stop ringing')
                    fail_str += '\ntdb ring-stop failed'
    except subprocess.CalledProcessError as err:
        traceback.format_exc()
        utils.debug(str(err))
        print err
    except KeyboardInterrupt:
        print '\nAborted by user\n'
        tdb.kill_tdb_server()
        time.sleep(0.05)
    finally:
        tdb.kill_tdb_server()
        time.sleep(0.05)

    if tdb_res == 10:
        utils.debug('All tdb commands PASS\n\n')
        utils.test_report('\n\nTDB test result:')
        utils.test_report('\nAll tdb commands PASS')
    else:
        utils.test_report('\n\nTDB test results: ')
        utils.test_report(pass_str + '\n')
        utils.test_report(fail_str + '\n\n')
