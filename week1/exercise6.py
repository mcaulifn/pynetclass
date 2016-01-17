#!/usr/bin/env python


import yaml, json

list1 = [1, 2, 3, 4, {"week": 1, "exercise": 6}]

with open ("exercise6.yml", "w") as yamlfile:
    yaml.dump(list1, yamlfile, default_flow_style=False)

with open ("exercise6.json", "w") as jsonfile:
    json.dump(list1, jsonfile)

