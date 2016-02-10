#!/usr/bin/env python
''' This module uses netmiko to run commands.'''

from getpass import getpass
import netmiko



def main():
    '''main'''
    
    rtr1 = {
        'device_type': 'cisco_ios',
        'ip': '50.76.53.27',
        'port': 22,
        'username': 'pyclass',
        'password': getpass(),
        }

    rtr2 = {
        'device_type': 'cisco_ios',
        'ip': '50.76.53.27',
        'port': 8022,
        'username': 'pyclass',
        'password': getpass(),
        }

    srx = {
        'device_type': 'juniper',
        'ip': '50.76.53.27',
        'port': 9822,
        'username': 'pyclass',
        'password': getpass(),
        }

    routerlist = [rtr1, rtr2, srx]
    
    for each in routerlist:
        conn = netmiko.ConnectHandler(**each)
    
        print(conn.send_command('show arp'))
        conn.disconnect()

if __name__ == "__main__":
    main()
