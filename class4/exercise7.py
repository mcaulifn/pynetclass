#!/usr/bin/env python
''' This module uses netmiko to run commands.'''

from getpass import getpass
import netmiko



def main():
    '''main'''

    rtr2 = {
        'device_type': 'cisco_ios',
        'ip': '50.76.53.27',
        'port': 8022,
        'username': 'pyclass',
        'password': getpass(),
        }

    routerlist = [rtr2]
    confchanges = ['logging buffered 37788']


    for each in routerlist:
        conn = netmiko.ConnectHandler(**each)

        print(conn.send_command('show run | i logging buff'))
        conn.send_config_set(confchanges)
        print(conn.send_command('show run | i logging buff'))
        conn.disconnect()

if __name__ == "__main__":
    main()
