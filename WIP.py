import subprocess


def popen(CMD, start_print, stop_print):
    print start_print
    p = subprocess.Popen(
        CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()
    if err:
        print(err)
        return 'ERROR'
    else:
        print(out)
        return out
    print stop_print


def checkcall(CMD, start_print, stop_print):
    print start_print
    p = subprocess.check_call(CMD, shell=True)
    print p
    print stop_print
