

"""
 Apaga todo menos el RTC
 RTV maximo 7horas, para mas import time
 Conecte el GPIO16 al Pin RST
 OJO RST, script de restablecimiento
"""

import machine

## Script restablecimiento
#if machine.reset_cause() == machine.DEEPSLEEP_RESET:
#    print('woke from a deep sleep')
#else:
#    print('power on or hard reset')


# configure RTC.ALARM0 to be able to wake the device
rtc = machine.RTC()
rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

# set RTC.ALARM0 to fire after 10 seconds (waking the device)
rtc.alarm(rtc.ALARM0, 10000)

# put the device to sleep
machine.deepsleep()
