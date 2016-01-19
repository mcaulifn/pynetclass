#!/usr/bin/env python


from ciscoconfparse import *
import re


parsedfile = CiscoConfParse("cisco_ipsec.txt")


crypto_map = parsedfile.find_objects(r"^crypto map")

no_aes_maps = []
temp = []

for each in crypto_map:
    child = each.re_search_children(r"set transform-set (?!AES)")
    if child:
        temp.append(each)
        temp.append(child)
        no_aes_maps.append(temp)

print(no_aes_maps)
