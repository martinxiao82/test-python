import mcu
import traceback
import subprocess
import os


name = ''
command = ''
path = ''
img = ''


# simple menu


def help_menu():
    print 30 * '-', 'menu', 30 * '-'
    print ''
    print 17 * ' ' + 'FOLLOWING COMMANDS ARE AVAILABLE:'
    print ''
    print 30 * ' ' + 'list'
    print ''
    print 30 * ' ' + 'erase'
    print ''
    print 30 * ' ' + 'upload'
    print ''
    print 30 * ' ' + 'test'
    print ''
    print 30 * ' ' + 'confirm'
    print ''
    print 30 * ' ' + 'reset'
    print ''
    print 30 * ' ' + 'list_bin'
    print ''
    print 67 * '-'


# mcumgr commands
def chose_file():
    os.path('/home/martin/trackr1/internal/firmware/smart-tag/build-PVT-ets')
    subprocess.check_call('ls', shell=True)
    file = raw_input('Choose bin file: ')
    path = '/home/martin/trackr1/internal/firmware/smart-tag/build-PVT-ets' + file
    return path
    os.path('')


def cmd_parser(input):

    if input == 'list':
        return mcu.img_list(name)

    elif input == 'erase':
        return mcu.img_erase(name)

    elif input == 'upload':
        return mcu.img_upload(name, path)

    elif input == 'test':
        return mcu.img_test(name, img)

    elif input == 'confirm':
        return mcu.img_confirm(name, img)

    elif input == 'reset':
        return mcu.reset()

    elif input == 'list_bin':
        chose_file()

    elif input == 'quit':
        print 'Bye bye!'

    else:
        print 'Try again!'


while command != 'quit':
    try:
        help_menu()
        command = raw_input('Enter command: ')
        cmd_parser(command)
    except (TypeError, subprocess.CalledProcessError, NameError) as detail:
        var = traceback.format_exc()
        print detail
    except KeyboardInterrupt:
        print 'Aborted by user'
        break
