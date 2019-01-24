import os


def setup():

    # Define PY_PATH as the path where all python scripts are
    os.environ['PY_PATH'] = os.environ['PWD'] + '/'
    # Root path for tracker as TRK_PATH
    os.chdir('../../../')
    os.environ['TRK_PATH'] = os.getcwd() + '/'
    # Define TDB_PATH as the path TDB can be executed
    os.environ['TDB_PATH'] = (os.environ['TRK_PATH'] + '/internal/tools/tdb/build/')
    # Define TAG_PATH as the path for smart-tag
    os.environ['TAG_PATH'] = (os.environ['TRK_PATH'] + '/internal/firmware/smart-tag/')
    # list all env paths
    print 'PY_PATH is: ' + os.environ['PY_PATH']
    print 'TRK_PATH is: ' + os.environ['TRK_PATH']
    print 'TDB_PATH is: ' + os.environ['TDB_PATH']
    print 'TAG_PATH is: ' + os.environ['TAG_PATH']


if __name__ == "__main__":
    setup()
