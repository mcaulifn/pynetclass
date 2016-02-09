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

    
    conn = netmiko.ConnectHandler(**rtr2)
    
    conn.config_mode()
    print("In config mode?")
    print(conn.check_config_mode())
    print("Current prompt:")
    print(conn.find_prompt())
    conn.exit_config_mode()
    conn.disconnect()

if __name__ == "__main__":
    main()
