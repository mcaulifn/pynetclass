#!/usr/bin/env python


import yaml, json

list1 = [1, 2, 3, 4, {"name": "exercise6", "class": 1}]

with open ("exercise6.yml", "w") as yamlfile:
    yaml.dump(list1, yamlfile, default_flow_style=False)

