#!/usr/bin/env python
'''
Write a script that connects to the lab pynet-rtr1, logins, and executes the
'show ip int brief' command.
'''

import telnetlib
import time
import socket
import sys
import getpass


class Router(object):
    """This class creates a telnet connection to a router
    along with the methods used to interact with that router"""

    def __init__(self, IP, USERNAME, PASSWORD, TELNET_TIMEOUT=10, TELNET_PORT=23):
        self.IP = IP
        self.USERNAME = USERNAME
        self.PASSWORD = PASSWORD
        self.TELNET_TIMEOUT = TELNET_TIMEOUT
        self.TELNET_PORT = TELNET_PORT

        self.remote_conn = self.telnet_connect()
        time.sleep(1)
        self.login()
        time.sleep(1)
        self.disable_paging()

    def send_command(self, cmd):
        '''
        Send a command down the telnet channel

        Return the response
        '''
        cmd = cmd.rstrip()
        self.remote_conn.write(cmd + '\n')
        time.sleep(1)
        return self.remote_conn.read_very_eager()

    def login(self):
        '''
        Login to network device
        '''

        output = self.remote_conn.read_until("sername:", self.TELNET_TIMEOUT)
        self.remote_conn.write(self.USERNAME + '\n')
        output += self.remote_conn.read_until("ssword:", self.TELNET_TIMEOUT)
        self.remote_conn.write(self.PASSWORD + '\n')
        return output

    def disable_paging(self, paging_cmd='terminal length 0'):
        '''
        Disable the paging of output (i.e. --More--)
        '''

        return self.send_command(paging_cmd)

    def telnet_connect(self):
        '''
        Establish telnet connection
        '''
        try:
            return telnetlib.Telnet(self.IP, self.TELNET_PORT, self.TELNET_TIMEOUT)
        except socket.timeout:
            sys.exit("Connection timed-out")

    def close_conn(self):
        ''' close connection'''
        self.remote_conn.close()


def main():
    '''
    Write a script that connects to the lab pynet-rtr1, logins, and executes the
    'show ip int brief' command.
    '''
    ip_addr = raw_input("IP address: ")
    ip_addr = ip_addr.strip()
    username = 'pyclass'
    password = getpass.getpass()

    rtr1 = Router(ip_addr, username, password)

    output = rtr1.send_command('show ip int brief')

    print "\n\n"
    print output
    print "\n\n"

    rtr1.close_conn()

if __name__ == "__main__":
    main()
