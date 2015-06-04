""""
Program to interact with Android Debug Bridge

contact: dtippman@visteon.com
"""
# Requires:
#    1.) Android SDK tools installed (https://developer.android.com/sdk/index.html)
#    2.) Phone with unlocked bootloader, SuperSU, Custom Recovery (CWM used for testing), and USB Debugging Enabled




import subprocess
import logging
import os 

##############################
# Location of ADB executable #
##############################
ADB_PATH = 'C:\Users\\atippmd\Desktop\custom_recovery\\adb-tools'

################
# ADB commands #
################
DEVICES = 'devices' # list connected devices

##################
# Shell Commands #
##################
KEYEVENT = 'shell input keyevent'

##############
# Key Events #
##############
KEYCODE = {'HOME' : '3',
           'BACK' : '4',
           'DPAD_UP' : '19',
           'DPAD_DOWN' : '20',
           'DPAD_LEFT' : '21',
           'DPAD_RIGHT' : '22',
           'POWER' : '26',
           'ENTER' : '66',
           'MENU' : '82',
           'SETTINGS' : '176',
           'WAKEUP' : '224',}

def send_adb_command(cmd):
    """
    Send a command to ADB.
    
    parameter:
    @ cmd: command string to execute 
    """       
    adb_process = subprocess.Popen(ADB_PATH + '\\adb ' + cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = adb_process.communicate()
    return_code = adb_process.wait()
    
    if return_code < 0:
        raise Exception("Unable to execute command.")
    return output, error
    
def input_keycode(code):
    send_adb_command(KEYEVENT + ' ' + KEYCODE[code])
    return
    
def wakeup_device():
    input_keycode('POWER')
    return

def unlock_device():
    input_keycode('MENU')
    
def bt_state():
    """
    Get state of bluetooth on device. 0=disabled. 1=enabled.
    """
    bt_state = int(send_adb_command('shell settings get global bluetooth_on')[0])
    return bt_state
    
def enable_bt():
    """
    Enable bluetooth on device.
    """
    
    if bt_state():
        logging.info("Bluetooth is already enabled.")
        return
        
    logging.info("Enabling bluetooth...")
    wakeup_device()
    unlock_device()
    ret = send_adb_command('shell am start -a android.bluetooth.adapter.action.REQUEST_ENABLE')
    assert 'Error' not in ret
    input_keycode('DPAD_RIGHT')
    input_keycode('DPAD_RIGHT')
    input_keycode('ENTER')
    if bt_state():
        logging.info("Bluetooth enabled")
        return
    logging.info("Bluetooth not enabled.")
    return

def main():
    """
    This is the main routine.
    """
    # Check if ADB path and executable are correct
    if not os.path.isfile(ADB_PATH+'\\adb.exe'):
        raise ValueError("ADB path not specified.")
    if "Android Debug Bridge version" not in send_adb_command('version')[0]:
        raise Exception("Cannot execute ADB.")
    if not int(send_adb_command('shell settings get global development_settings_enabled')[0]):
        print("Developer options not enabled on device.")
        exit()
    
    enable_bt()
    # input_keycode('WAKEUP') # Wakeup device
    # input_keycode('MENU') # Unlock touchscreen
    # input_keycode('HOME')
    # input_keycode('MENU')
    # input_keycode(KEYCODE_DPAD_DOWN) # Unlock touchscreen
    # input_keycode(KEYCODE_DPAD_DOWN) # Unlock touchscreen
    # input_keycode(KEYCODE_ENTER) # Unlock touchscreen
    # input_keycode(KEYCODE['SETTINGS'])
    
main()