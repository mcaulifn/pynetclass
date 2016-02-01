#!/usr/bin/env python
'''
This script polls a router for 30 minutes and creates graph a graph for four counters.
'''

from snmp_helper import snmp_get_oid_v3, snmp_extract
from time import gmtime, strftime
import pygal


'''
Poll devices
write data
write graph
wait
repeat
'''

def poll():
    pass

def writefile():
    pass

def writegraph():
    pass

def wait():
    pass

def main():
'''
main function
'''

    poll()
    writefile()
    writegraph()
    wait() #do i need a wait function?


if __name__ == "__main__":
    main()
