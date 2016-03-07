#/usr/bin/env python
'''run show arp on each device ind db'''

from __future__ import print_function
import django
from datetime import datetime
from net_system.models import NetworkDevice


def main():
    '''main'''

    django.setup()

    starttime = datetime.now()
    for each in NetworkDevice.objects.all():
        conn = netmiko.ConnectHandler(**each)

        print(conn.send_command('show arp'))
        conn.disconnect()
    print("Elapsed time: %s" %str(datetime.now()-starttime))
        
if __name__ == "__main__":
    main()
