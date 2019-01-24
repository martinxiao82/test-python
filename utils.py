#!/usr/bin/python
import os
import smtplib
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import re
import shutil


# Function that checks whether the input string is a MAC
def check_MAC(MAC):
    if re.match("[0-9a-f]{2}(:?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", MAC.lower()):
        return True
    else:
        print '\nInput is NOT a MAC! Please try again!'
        return False


def debug(msg):
    print msg
    filename = 'debug.txt'
    f = open(os.path.join(os.environ['SCRIPT_PATH'], filename), 'a')
    msg = '\n' + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + \
        ' ' + msg
    f.write(msg)
    f.close()


def create_boot_log_file(boot_log, build_no):
    # for future use, we can attach boot log if the test fails
    log_file_name = "log_" + datetime.now().strftime('%Y-%m-%d') + \
        "_" + build_no + ".txt"
    log_file = open(log_file_name, "a")
    log_file.write(boot_log)
    log_file.close()


def flash_report(build_no, verdict, msg):
    filename = 'temp_result.txt'
    message = '\n' + '\nBuild number: ' + build_no + \
        '\nVerdict: ' + verdict + '\nLog: ' + msg
    f = open(filename, 'a')
    f.write(message)
    f.close()


def test_report(msg):
    filename = 'temp_result.txt'
    f = open(os.path.join(os.environ['SCRIPT_PATH'], filename), 'a')
    f.write(msg)
    f.close()


# open smtp server.
def send_email():
    with open('email.txt') as f:
        recipient = [line.strip() for line in f]
    msg = MIMEMultipart()
    msg['FROM'] = 'trackr.nightly@sigma.se'
    msg['TO'] = ", ".join(recipient)
    msg['SUBJECT'] = '[Automatic Nightly Test]'

    with open('temp_result.txt', 'r') as f:
        TEXT = f.read()
    msg.attach(MIMEText(TEXT))

    debug('Result:' + TEXT)

    # If the size of debug.txt is > 10MB,
    # saves it in folder "Trackr_Result" in home folder
    # and removes it from /test folder
    debug_file_size = os.stat('debug.txt').st_size
    max_size = 10 * 1024 ** 2
    if debug_file_size > max_size:
        print 'file size exceeds'
        if not os.path.exists(os.environ['RESULT_PATH']):
            os.makedirs(os.environ['RESULT_PATH'])
        shutil.copy('debug.txt', os.environ['RESULT_PATH'],)
        os.remove('debug.txt')

    # If "debug.txt" exists in /test folder (file size <= 10MB)
    # attaches it in the mail
    if os.path.isfile(os.environ['DEBUG_PATH']) is True:
        with open('debug.txt', 'r') as f:
            txt_attachment = MIMEText(f.read())
            txt_attachment.add_header('Content-Disposition', 'attachment',
                                      filename='debug.txt')
            msg.attach(txt_attachment)

    try:
        server = smtplib.SMTP()
        server.connect('smtp.cypoint.net', '25')
        server.ehlo()
        server.sendmail(msg['FROM'], recipient, msg.as_string())
        server.close()
    except Exception as e:
        if not os.path.exists(os.environ['RESULT_PATH']):
            os.makedirs(os.environ['RESULT_PATH'])
        with open(os.path.join(os.environ['RESULT_PATH'],
                  'email_status_fail.txt'), 'a') as f:
            f.write(datetime.now().strftime('%Y-%m-%d') +
                    ' Error: ' + str(e) + '\nMessage: ' + TEXT + '\n')
        shutil.copy('debug.txt', os.environ['RESULT_PATH'])


# Set up enviroment using envsetup bash script
# For future ref, better to port bash script to python.
def env_setup(path):
    SOURCE_CMD = 'bash envsetup.sh'
    os.chdir(path)
    subprocess.check_call(SOURCE_CMD, shell=True)


def reset_head(path):
    RESET_CMD = 'git reset --hard HEAD^'
    os.chdir(path)
    print 'reseting repo...'
    subprocess.check_call(RESET_CMD, shell=True)


def repo_sync(path):
    REPO_CMD = 'repo sync'
    os.chdir(path)
    print 'making a repo sync ...'
    subprocess.check_call(REPO_CMD, shell=True)


# Build and flash using build.sh scrpt, for future work, port to python.
def build_and_flash(path, variant):
    # BUILD_CMD = ' ./build.sh clean boot ' + variant + ' --ota-verification'
    # BUILD_FLASH_CMD = ' ./build.sh boot ' + variant + ' flash' + ' --factory'
    BUILD_CMD = ' ./build.sh clean boot ' + variant
    BUILD_FLASH_CMD = './build.sh clean boot pvt flash'
    os.chdir(path)
    print 'building and flashing'
    # Build
    subprocess.check_call(BUILD_CMD, shell=True)
    # Find the bin file for OTA in /build-PVT folder
    ota_fw_path = find_bin_file(os.environ['FW_PATH'])
    # Copy OTA bin file to /trackr folder
    shutil.copy(ota_fw_path, os.environ['TRACKR_PATH'])
    # Build and flash
    subprocess.check_call(BUILD_FLASH_CMD, shell=True)


def reset(path):
    reset_CMD = './nrfjprog -r'
    print 'Reseting DUT'
    os.chdir(path)
    subprocess.check_call(reset_CMD, shell=True)


def get_build_version(path):
    CMD = 'git describe'
    os.chdir(path)
    pipe = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE).stdout
    version = pipe.read()
    res = version.split('-')
    res1 = '.'.join(res[0].split('.')[:2])
    result = '.'.join([res1, res[1]])
    return result


def find_bin_file(path):
    for file in os.listdir(path):
        if file.endswith('.bin') and 'signed_PVT_OTA' in file:
            ota_fw_path = os.path.join(path, file)
    return ota_fw_path
