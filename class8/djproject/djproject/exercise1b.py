#/usr/bin/env python
'''Assigns the correct credentials to the network devices'''

from __future__ import print_function
import django
from net_system.models import NetworkDevice, Credentials


def main():
    '''main'''

    django.setup()

    for device in NetworkDevice.objects.all():
        if device.device_type == 'cisco_ios':
            device.credentials = Credentials.objects.get(username='pyclass')
        elif device.device_type == 'juniper':
            device.credentials = Credentials.objects.get(username='pyclass')
        elif device.device_type == 'arista_eos':
            device.credentials = Credentials.objects.get(username='admin1')
        device.save()
        print('%s : %s' %(device.device_name, device.credentials))

if __name__ == "__main__":
    main()
