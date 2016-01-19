#!/usr/bin/env python

from ciscoconfparse import *
import re


parsedfile = CiscoConfParse("cisco_ipsec.txt")


crypto_map = parsedfile.find_objects_wo_child(r"^crypto map", r"set transform-set AES.*")

for each in crypto_map:
	for child in each.children:
		match = re.search(r"^ set transform-set (.*)$", child.text)
		if match:
			print(each.text + " -- " + match.group(1))
