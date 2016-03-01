#!/usr/bin/env python
from __future__ import print_function
from pprint import pprint
import pyeapi
import sys
import argparse

def enable_cmds(conn, cmds):
    '''run commands in enable mode, return output'''
    try:
        output = conn.enable(cmds)
        return strip_output(output)
    except (pyeapi.eapilib.CommandError, KeyError):
        return False


def conf_cmds(conn, cmds):
    '''run configuration commands'''
    return conn.config(cmds)

def strip_output(output):
    '''remove extra wrappers on output'''
    return output[0]['result']

def main():

    node = pyeapi.connect_to('pynet-sw3')

    #Creating parser for run-time variables
    parser = argparse.ArgumentParser(description="Add/remove VLAN")
    parser.add_argument("vlan_id", help="VLAN number to create or remove", action="store", type=int)
    parser.add_argument('-name', action='store', dest='vlan_name', help='Name of VLAN')
    parser.add_argument("--remove", action="store_true", help="Remove the supplied VLAN ID")

    #Parsing input
    c_args = parser.parse_args()
    vlan_id = c_args.vlan_id
    vlan_name = c_args.vlan_name
    remove = c_args.remove

    #Check if vlan exists
    vlan_exists = enable_cmds(node, 'show vlan id %s' % vlan_id)
    vlan_exists = vlan_exists['vlans']

    if remove:
        #if the remove flag was specified and the vlan exists, delete it.
        if vlan_exists:
            print("VLAN %s is configured. Deleting." % vlan_id)
            conf_cmds(node, ['no vlan %s' %vlan_id])
        #if the vlan does not exist, nothing to delete...
        else:
            print("VLAN %s is not configured. Nothing to delete." % vlan_id)
    else:
        #if the remove flag was not specified and vlan exists, do nothing
        if vlan_exists:
            print("VLAN %s is already configured." % vlan_id)
        #if the vlan does not exist, create it.
        else:
            print("VLAN %s is not configured. Adding." % vlan_id)
            if vlan_name is not None:
                conf_cmds(node, ['vlan %s' %vlan_id, 'name %s' % vlan_name])
            else:
                conf_cmds(node, ['vlan %s' %vlan_id])


if __name__ == "__main__":
    main()
