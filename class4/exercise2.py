#!/usr/bin/env python
""" This module uses telnet to log in to a router and run the show ver command."""


from time import sleep
from getpass import getpass
import sys
import socket
import paramiko

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
        if self.conn.recv_ready():
            self.conn.recv(MAX_BUFFER)
        self.run_cmd("terminal length 0")

    def login(self):
        """Creates the telnet connection and logs in to the device"""

        try:
            conn_pre = paramiko.SSHClient()
            conn_pre.load_system_host_keys()

            conn_pre.connect(self.ip, port=self.port, username=self.creds[0], password=self.creds[1],
                             allow_agent=False, look_for_keys=False)
            conn = conn_pre.invoke_shell()
            conn.keep_this = conn_pre

        except socket.timeout:
            sys.exit("Connection timed-out")

        return conn


    def run_cmd(self, cmd='', pause=3):
        """run command that is passed in"""

        cmd = cmd.strip()

        self.conn.send(cmd + "\n")
        sleep(pause)

        if self.conn.recv_ready():
            return self.conn.recv(MAX_BUFFER)
        else:
            return ''

    def config_mode_enter(self):
        '''Enters into config mode'''

        return self.run_cmd('config t', pause=1)

    def config_mode_exit(self):
        '''Enters into config mode'''

        return self.run_cmd('end', pause=1)

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
    print(rtr.run_cmd('show run | i logging'))

    #change logging buffer size
    rtr.config_mode_enter()
    rtr.run_cmd('logging buffered 37789')
    rtr.config_mode_exit()

    #print new logging config
    print(rtr.run_cmd('show run | i logging'))

    rtr.close_conn()


if __name__ == "__main__":
    main()
