#/usr/bin/env python
'''Adds new devices to db'''

from __future__ import print_function
import django
from net_system.models import NetworkDevice

def main():
    '''main'''
    django.setup()

    pynet_rtrtest01 = NetworkDevice(
        device_name='pynet-rtrtest01',
        device_type='cisco_ios',
        ip_address='50.76.53.27',
        port=10022,
    )
    pynet_rtrtest01.save()

    pynet_rtrtest02 = NetworkDevice.objects.get_or_create(
        device_name='pynet-rtrtest02',
        device_type='cisco_ios',
        ip_address='50.76.53.27',
        port=11022,
    )

    for device in NetworkDevice.objects.all():
        print(device.device_name)

if __name__ == "__main__":
    main()
