#!/usr/bin/env python
from __future__ import print_function
from pprint import pprint
import pyeapi
import sys


node = pyeapi.connect_to('pynet-sw3')

ints = node.enable('show interfaces')

int_data = {}

for key in ints[0]['result']['interfaces'].iterkeys():
    inOctets = ''
    outOctets = ''
    try:
        inOctets = ints[0]['result']['interfaces'][key]['interfaceCounters']['inOctets']
        outOctets = ints[0]['result']['interfaces'][key]['interfaceCounters']['outOctets']
        int_data[key] = {'inOctets':inOctets, 'outOctets':outOctets}
    except KeyError:
        print("Data not found for %s" % key)

pprint(int_data)