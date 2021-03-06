#!/usr/bin/env python
""" This module uses telnet to log in to a router and run the show ip int bri command."""


import telnetlib
import time
import getpass
import sys
import re
import socket


def login(routerip, port, timeout, creds):
    """Creates the telnet connection and logs in to the device"""

    try:
        conn = telnetlib.Telnet(routerip, port, timeout)

    except socket.timeout:
        sys.exit("Connection timed-out")

    output = conn.read_until("Username:", 10)
    conn.write(creds[0] + "\n")
    time.sleep(1)

    output = conn.read_until("Password:", 10)
    conn.write(creds[1] + "\n")
    time.sleep(6)

    output = conn.read_very_eager()

    auth_fail_match = re.search(r".*\s*\% Authentication failed\s*Username\:", output)

    if auth_fail_match:
        conn.close()
        sys.exit("Authentication failed")
    return conn


def run_cmd(conn, cmd):
    """run command that is passed in"""

    cmd = cmd.rstrip()

    conn.write(cmd + "\n")
    time.sleep(3)

    return conn.read_very_eager()

def main():
    """main function"""

    creds = ("pyclass", getpass.getpass("enter password: "))
    routerip = "50.76.53.27"
    TELNET_TIMEOUT = 5
    TELNET_PORT = 23

    #initiate connection and login
    router_telnet = login(routerip, TELNET_PORT, TELNET_TIMEOUT, creds)


    #disable paging
    run_cmd(router_telnet, "terminal length 0")

    output = run_cmd(router_telnet, "show ip int brief")

    print(output)

    router_telnet.close()


if __name__ == "__main__":
    main()
