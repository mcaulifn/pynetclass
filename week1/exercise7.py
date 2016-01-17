#!/usr/bin/env python


#from __future__ import print_function
import yaml, json
from pprint import pprint

def print_out(data_type, data):
    
    print("Here is the %s data:" %data_type)
    
    pprint(data)


with open ("exercise6.yml") as yamlfile:
    yamldata = yaml.load(yamlfile)

print_out("yaml", yamldata)


with open ("exercise6.json") as jsonfile:
    jsondata = json.load(jsonfile)

print_out("json", jsondata)
