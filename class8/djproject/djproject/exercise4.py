#/usr/bin/env python
'''Adds new devices to db'''

from __future__ import print_function
import django
from net_system.models import NetworkDevice

def main():
    '''main'''
    django.setup()

    try:
        NetworkDevice.objects.get(device_name='pynet-rtrtest01').delete()
        NetworkDevice.objects.get(device_name='pynet-rtrtest02').delete()
    except NetworkDevice.DoesNotExist:
        pass

    for device in NetworkDevice.objects.all():
        print(device.device_name)

if __name__ == "__main__":
    main()
