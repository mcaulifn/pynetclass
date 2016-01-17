#!/usr/bin/env python


from __future__ import print_function
from ciscoconfparse import CiscoConfParse


parsedfile = CiscoConfParse("cisco_ipsec.txt")


crypto_map = parsedfile.find_objects(r"^crypto map CRYPTO")


for each in crypto_map:
    print(each.text)
    for child in each.children:
        print(child.text)
