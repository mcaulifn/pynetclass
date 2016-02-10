#!/usr/bin/env python
""" This module uses telnet to log in to a router and run the show ver command."""


from time import sleep
from getpass import getpass
import sys
import socket
import pexpect

MAX_BUFFER = 65535

class Router(object):
    '''
    this class creates a router instance, logs in to the device
    and changes term length to 0
    '''
    def __init__(self, ip, creds, port=22):
        self.ip = ip
        self.creds = creds
        self.port = port

        #call methods to establish connection
        self.conn = self.login()
        self.prompt = self.find_prompt()
        self.run_cmd("terminal length 0")

    def login(self):
        """Creates the connection and logs in to the device"""

        try:
            conn = pexpect.spawn('/usr/bin/ssh', ['-l', self.creds[0], self.ip, '-p', str(self.port)])
            conn.timeout = 4

            conn.expect('ssword:')
            conn.sendline(self.creds[1])
            conn.expect('#')

        except socket.timeout:
            sys.exit("Connection timed-out")

        return conn

    def find_prompt(self):
        '''
        Find prompt
        '''

        self.conn.send('\n')
        sleep(1)
        self.conn.expect('#')
        prompt = self.conn.before + self.conn.after
        return prompt.strip()

    def run_cmd(self, cmd='', conf=False):
        """run command that is passed in"""

        cmd = cmd.strip()

        if conf:
            p = self.find_prompt()
            self.conn.sendline(cmd)
            self.conn.expect_exact(p)
        else:
            p = self.prompt
            self.conn.sendline(cmd)
            self.conn.expect(p)

        return self.conn.before


    def config_mode_enter(self):
        '''Enters into config mode'''

        self.conn.sendline('config t')
        self.conn.expect('#')

        return self.conn.before

    def config_mode_exit(self):
        '''Enters into config mode'''

        return self.run_cmd('end')

    def save_config(self):
        '''saves running config to startup config'''

        return self.run_cmd('copy running-config startup-config')

    def close_conn(self):
        '''close connection'''

        return self.conn.close()

def main():
    """main function"""

    creds = ('pyclass', getpass("enter password: "))
    routerip = '50.76.53.27'
    port = 8022

    #initiate connection and login
    rtr = Router(routerip, creds, port=port)

    #print current logging config
    print(rtr.run_cmd('show run | i logging buffered'))

    #change logging buffer size
    rtr.config_mode_enter()
    rtr.run_cmd('logging buffered 37788', conf=True)
    rtr.config_mode_exit()

    #print new logging config
    print(rtr.run_cmd('show run | i logging buffered'))

    rtr.close_conn()


if __name__ == "__main__":
    main()
