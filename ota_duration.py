#!/usr/bin/python
import mcu
import env_setup
import os

# defines
iterations = None
nbr_fails = None
nbr_sucess = None
tot_time = None
avg_time = None
name = None
image = None
runs = None
path = None


def setup():
    global runs
    global iterations
    global path
    global name
    env_setup.setup()
    path = os.environ['PY_PATH']
    iterations = raw_input('Number of interations:')
    name = raw_input('Enter name of device:')
    runs = 0
    print mcu.img_list(name)


if __name__ == "__main__":
    try:
        setup()
        while runs <= iterations:
            runs += 1
    except Exception as detail:
        raise detail
