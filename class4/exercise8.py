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

    routerlist = [rtr1, rtr2]


    for each in routerlist:
        conn = netmiko.ConnectHandler(**each)

        print(conn.send_command('show run | i logging buff'))
        print(conn.send_command('show run | i logging con'))
        conn.send_config_from_file(config_file='rtrchanges.txt')
        print(conn.send_command('show run | i logging buff'))
        print(conn.send_command('show run | i logging con'))
        conn.disconnect()

if __name__ == "__main__":
    main()
