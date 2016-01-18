#!/usr/bin/env python


from __future__ import print_function
from ciscoconfparse import CiscoConfParse


parsedfile = CiscoConfParse("cisco_ipsec.txt")


crypto_map = parsedfile.find_objects(r"^crypto map")

pfs_maps = []

for each in crypto_map:
    if each.re_search_children(r"set pfs group2"):
        pfs_maps.append(each)

print(pfs_maps)
