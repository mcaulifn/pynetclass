#!/usr/bin/env python


import yaml, json, pprint

pp = pprint.PrettyPrinter(indent=4)

print("Here is the YAML data:")
with open ("exercise6.yml") as yamlfile:
    pprint.pprint(yaml.load(yamlfile), indent=4)

print("Here is the JSON data:")
with open ("exercise6.json") as jsonfile:
    pprint.pprint(json.load(jsonfile), indent=4)

