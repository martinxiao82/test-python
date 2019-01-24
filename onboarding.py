import tdb
import os


# set up variables
MAC = raw_input('input MAC: ')
os.environ['TDB_PATH'] = '/home/martin/trackr1/internal/tools/tdb/build'

# step to right path
os.chdir(os.environ['TDB_PATH'])


tdb.start_scan()
tdb.connect(MAC)
# tdb.ble_param(MAC, '20 40 0 3200 23')
tdb.onboard_start(MAC)
tdb.onboard_confirm(MAC)
