#/usr/bin/env python
'''Assigns the correct vendor to the network devices'''

from __future__ import print_function
import django
from net_system.models import NetworkDevice


def main():
    '''main'''

    django.setup()

    for device in NetworkDevice.objects.all():
        if device.device_type == 'cisco_ios':
            device.vendor = 'cisco'
        elif device.device_type == 'juniper':
            device.vendor = 'juniper'
        elif device.device_type == 'arista_eos':
            device.vendor = 'arista'
        device.save()
        print('%s : %s' %(device.device_name, device.vendor))

if __name__ == "__main__":
    main()
