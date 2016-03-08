#/usr/bin/env python
'''run show version on each device in db'''

from __future__ import print_function
from datetime import datetime
import threading
import django
from net_system.models import NetworkDevice, Credentials
import netmiko

def run_command_thread(device, cmd):
    '''run command in a threaded env'''

    print('*' * 80)
    conn = netmiko.ConnectHandler(device_type=device.device_type, ip=device.ip_address,
                                  username=device.credentials.username, password=device.credentials.password,
                                  port=device.port)
    print(conn.send_command(cmd))
    conn.disconnect()

def main():
    '''main'''

    django.setup()

    command = 'show version'

    starttime = datetime.now()
    for each in NetworkDevice.objects.all():
        c_thread = threading.Thread(target=run_command_thread, args=(each,command))
        c_thread.start()

    main_thread = threading.currentThread()

    for each_thread in threading.enumerate():
        if each_thread != main_thread:
            each_thread.join()

    print("Elapsed time: %s" %str(datetime.now()-starttime))

if __name__ == "__main__":
    main()
