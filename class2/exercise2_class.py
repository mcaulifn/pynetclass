#!/usr/bin/env python
""" This module uses telnet to log in to a router and run the show ip int bri command."""


import telnetlib
import time
import getpass
import sys
import re
import socket

class Router(object):
    '''
    this class creates a router instance, logs in to the device
    and changes term length to 0
    '''
    def __init__(self, ip, creds, TELNET_TIMEOUT=5, TELNET_PORT=23):
        self.ip = ip
        self.creds = creds
        self.TELNET_TIMEOUT = TELNET_TIMEOUT
        self.TELNET_PORT = TELNET_PORT

        #call methods to establish connection
        self.conn = self.login()
        self.run_cmd("terminal length 0")

    def login(self):
        """Creates the telnet connection and logs in to the device"""

        try:
            conn = telnetlib.Telnet(self.ip, self.TELNET_PORT, self.TELNET_TIMEOUT)

        except socket.timeout:
            sys.exit("Connection timed-out")

        output = conn.read_until("Username:", 10)
        conn.write(self.creds[0] + "\n")
        time.sleep(1)

        output = conn.read_until("Password:", 10)
        conn.write(self.creds[1] + "\n")
        time.sleep(6)

        output = conn.read_very_eager()

        auth_fail_match = re.search(r".*\s*\% Authentication failed\s*Username\:", output)

        if auth_fail_match:
            conn.close()
            sys.exit("Authentication failed")
        return conn


    def run_cmd(self, cmd):
        """run command that is passed in"""

        cmd = cmd.rstrip()

        self.conn.write(cmd + "\n")
        time.sleep(3)

        return self.conn.read_very_eager()

    def close_conn(self):
        '''close connection'''

        return self.conn.close()

def main():
    """main function"""

    creds = ("pyclass", getpass.getpass("enter password: "))
    routerip = "50.76.53.27"

    #initiate connection and login
    rtr = Router(routerip, creds)

    output = rtr.run_cmd("show ip int brief")

    print(output)

    rtr.close_conn()


if __name__ == "__main__":
    main()
