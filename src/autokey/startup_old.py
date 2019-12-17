'''
Script to run on every startup
'''

import platform, socket, re, uuid, json, psutil, pyautogui, os, pwd, subprocess, sys, mcs, time, pyperclip


def get_system_info():
    try:
        info={}
        info['platform']=platform.system()
        info['platform-release']=platform.release()
        info['platform-version']=platform.version()
        info['architecture']=platform.machine()
        info['hostname']=socket.gethostname()
        info['ip-address']=socket.gethostbyname(socket.gethostname())
        info['mac-address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor']=platform.processor()
        info['ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        return info
    except Exception as e:
        logging.exception(e)

def get_username():
    return pwd.getpwuid(os.getuid())[0]

def cmd(command):
    c = subprocess.run(command, shell=True, capture_output=True, text=True)
    result = [c.stdout.strip(), c.stderr.strip()]
    return result

system_info = get_system_info()
print(system_info)
# Currently only support Linux
if system_info['platform'] == 'Linux':

    # Check in what computer the script is running
    if system_info['hostname'] == 'uracila':
        if get_username() == 'mcsouza':

            print(os.path.split(sys.argv[0]))


        else:
        	pass
    elif system_info['hostname'] == 'matheus-acer':
        if get_username() == 'matheus':

    else:
        pass

else:
    pyautogui.alert(title='Error', text="This program currently doesn't work on windows")
