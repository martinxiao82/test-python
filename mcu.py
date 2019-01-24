import subprocess
import traceback
import utils

retries = 5


def img_list(name):
    CMD = 'sudo ./mcumgr --conntype ble -t 30 --connstring peer_name=' + \
        name + ' image list'
    utils.debug('Listing image for: ' + name)
    for i in range(retries):
        utils.debug('Loop: ' + str(i))
        proc = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        (out, err) = proc.communicate()
        if err:
            utils.debug(err)
        else:
            break
    if proc.returncode != 0:
        return 'FAIL'
    else:
        utils.debug(out)
        return out


def img_erase(name):
    CMD = 'sudo ./mcumgr --conntype ble -t 30 --connstring peer_name=' + \
        name + ' image erase'
    utils.debug('Erasing slot 1 for: ' + name)
    for i in range(retries):
        utils.debug('Loop: ' + str(i))
        try:
            result = subprocess.check_call(CMD, shell=True)
        except (subprocess.CalledProcessError) as err:
            traceback.format_exc()
            utils.debug(str(err))
            if i < retries - 1:
                continue
            else:
                raise
        break
    utils.debug(str(result))


def img_upload(name, path):
    CMD = 'sudo ./mcumgr --conntype ble -t 30 --connstring peer_name=' + \
        name + ' image upload ' + path
    utils.debug('Uploading to: ' + name)
    for i in range(retries):
        utils.debug('Loop: ' + str(i))
        try:
            result = subprocess.check_call(CMD, shell=True)
        except (subprocess.CalledProcessError) as detail:
            traceback.format_exc()
            utils.debug(str(detail))
            if i < retries - 1:
                continue
            else:
                raise
        break
    utils.debug(str(result))


def img_test(name, img_hash):
    CMD = 'sudo ./mcumgr --conntype ble -t 30 --connstring peer_name=' + \
        name + ' image test ' + img_hash
    utils.debug('Running the new image for: ' + name)
    for i in range(retries):
        utils.debug('Loop: ' + str(i))
        try:
            result = subprocess.check_call(CMD, shell=True)
        except (subprocess.CalledProcessError) as detail:
            traceback.format_exc()
            utils.debug(str(detail))
            if i < retries - 1:
                continue
            else:
                raise
        break
    utils.debug(str(result))


def img_confirm(name, img):
    CMD = 'sudo ./mcumgr --conntype ble -t 30 --connstring peer_name=' + \
        name + ' image confirm ' + img
    utils.debug('Confirming image for: ' + name)
    for i in range(retries):
        utils.debug('Loop: ' + str(i))
        try:
            result = subprocess.check_call(CMD, shell=True)
        except (subprocess.CalledProcessError) as detail:
            traceback.format_exc()
            utils.debug((detail))
            if i < retries - 1:
                continue
            else:
                raise
        break
    utils.debug(str(result))


def reset(name):
    CMD = 'sudo ./mcumgr --conntype ble -t 30 --connstring peer_name=' + \
        name + ' reset'
    utils.debug('Reseting : ' + name)
    for i in range(retries):
        utils.debug('Loop: ' + str(i))
        try:
            result = subprocess.check_call(CMD, shell=True)
        except (subprocess.CalledProcessError) as detail:
            traceback.format_exc()
            utils.debug(str(detail))
            if i < retries - 1:
                continue
            else:
                raise
        break
    utils.debug(str(result))
