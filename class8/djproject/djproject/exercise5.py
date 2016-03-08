#/usr/bin/env python
'''run show arp on each device ind db'''

from __future__ import print_function
from datetime import datetime
import django
from net_system.models import NetworkDevice, Credentials
import netmiko


def main():
    '''main'''

    django.setup()

    starttime = datetime.now()
    for each in NetworkDevice.objects.all():
        print('*' * 80)
        conn = netmiko.ConnectHandler(device_type=each.device_type, ip=each.ip_address,
                                      username=each.credentials.username, password=each.credentials.password,
                                      port=each.port)

        print(conn.send_command('show version'))
        conn.disconnect()

    print("Elapsed time: %s" %str(datetime.now()-starttime))

if __name__ == "__main__":
    main()
