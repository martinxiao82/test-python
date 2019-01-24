#!/usr/bin/python
import time
import os
import utils
import mcu
import traceback
import subprocess


os.environ['FW_PATH'] = 'internal/firmware/smart-tag/build-PVT-qa'
p_name = 'SmartTag-test'


def main():
    utils.debug('\n\n******OTA TEST******\n')

    # Steps to TRACKR_PATH which contains mcumgr
    os.chdir(os.environ['TRACKR_PATH'])

    try:
        # Queries device for its current image list
        img_list = mcu.img_list(p_name)
        time.sleep(0.5)

        # Erases image in slot 1 if exist
        if 'slot=1' in img_list:
            mcu.img_erase(p_name)
            time.sleep(0.5)

        # Uploads new image to DUT
        os.environ['OTA_FW_PATH'] = utils.find_bin_file(os.environ
                                                        ['TRACKR_PATH'])
        mcu.img_upload(p_name, os.environ['OTA_FW_PATH'])

        # Checks current image list
        curr_img_list = mcu.img_list(p_name)
        time.sleep(0.5)

        if 'slot=1' in curr_img_list:
            utils.debug('Image is successfully uploaded to slot 1\n')
            # Extracts slot1's hash from the current image list
            slot1_str = curr_img_list.split('slot=1')[1]
            slot1_hash = slot1_str.split('hash: ')[1].split('\n')[0]
            slot1_hash = slot1_hash.replace('\n', '')
        else:
            utils.debug('FAIL to upload image!\n')

        # Tells DUT to run the new image on its next boot
        mcu.img_test(p_name, slot1_hash)

        # Makes the image swap permanent
        mcu.img_confirm(p_name, slot1_hash)
        time.sleep(0.5)

        # Resets DUT
        mcu.reset(p_name)
        time.sleep(5)

        # Checks the image list after reset
        curr_img_list = mcu.img_list(p_name)
        time.sleep(1)

        slot0_str = curr_img_list.split('slot=1')[0]
        slot0_hash = slot0_str.split('hash: ')[1]
        slot0_hash = slot0_hash.replace('\n', '')
        if ' ' in slot0_hash:
            slot0_hash = slot0_hash.replace(' ', '')

        if (slot0_hash == slot1_hash):
            utils.debug('FW upgrade successful\n')
            utils.test_report('\n\nFW upgrade successful\n\n')
        else:
            utils.debug('Failed to upgrade FW!!!\n')
            utils.test_report('\n\nFailed to upgrade FW!!!\n\n')

        # Erases the image in slot 1
        mcu.img_erase(p_name)

        curr_img_list = mcu.img_list(p_name)
        time.sleep(0.5)

        if os.path.exists(os.environ['OTA_FW_PATH']):
            os.remove(os.environ['OTA_FW_PATH'])
    except (subprocess.CalledProcessError, UnboundLocalError) as detail:
        traceback.format_exc()
        utils.debug(str(detail))
        utils.debug('Failed to upgrade FW!!!\n')
        utils.test_report('\n\nFailed to upgrade FW!!!\n\n')
    except KeyboardInterrupt:
        utils.debug('\nAborted by user\n')


if __name__ == '__main__':
    main()
