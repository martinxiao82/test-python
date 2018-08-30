#!/usr/bin/python 

import os
import sys
import smtplib
import subprocess
from datetime import datetime


def debug(msg):
    print "Debug: " + msg

def create_boot_log_file(boot_log, build_no):
    #for future use, we can attach boot log if the test fails
    log_file_name = "log_" + datetime.now().strftime('%Y-%m-%d') + "_" + build_no + ".txt"
    log_file = open(log_file_name, "a")
    log_file.write(boot_log)
    log_file.close()

def report(build_no, verdict, msg):
    filename = 'temp_result.txt'
    message =  '\n\n' + '\nBuild number: '+ build_no + '\nVerdict: ' + verdict + '\nLog: ' + msg
    f = open(filename, 'a')
    f.write(message)
    f.close()

# open smtp server.
def send_email():
    recipient = [line.strip() for line in open('email.txt')]

    FROM = 'trackr.nightly@sigma.se'
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = '[Automatic Nightly Test]'
    TEXT = open('temp_result.txt', 'r').read()
    debug('Result:' + TEXT)

    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP()
        server.connect('smtp.cypoint.net', '25')
        server.ehlo()
        server.sendmail(FROM, TO, message)
        server.close()
    except Exception as e:
        f = open('email_status_fail.txt', 'a')
        f.write(datetime.now().strftime('%Y-%m-%d') + ' Error: ' + str(e) + ' Message: ' + TEXT + '\n')
        f.close()

# set up enviroment using envsetup bash script, for future ref, better to port bash script to python.
def env_setup(path):
    source_cmd = 'bash envsetup.sh'
    os.chdir(path)
    subprocess.call(source_cmd, shell=True)

def repo_sync(path):
    repo_cmd = 'repo sync'
    os.chdir(path)
    print 'making a repo sync ...'
    subprocess.call(repo_cmd, shell=True)

# Build and flash using build.sh scrpt, for future work, port to python.
def build_and_flash(path, variant):
    build_flash_cmd = ' ./build.sh boot ' + variant +' flash' + ' --ets'
    os.chdir(path)
    print 'building and flashing'
    subprocess.call(build_flash_cmd, shell=True)

def get_build_version(path):
    cmd = 'git describe'
    path = '~/trackr1/internal/firmware/smart-tag/'
    os.chdir(path)
    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
    version = pipe.read()
    result = version[0:1]+'.'+version[2:3] +'.'+version[4:6]
    return result
    


    

