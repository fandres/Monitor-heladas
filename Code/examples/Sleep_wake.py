

""" SCRIPT DESPERTAR DE  SLEEP """
import machine 

# Script restablecimiento
if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('woke from a deep sleep')
else:
    print('power on or hard reset')
