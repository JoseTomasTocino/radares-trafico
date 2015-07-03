#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import data
import io
import json

base_url = "http://infocar.dgt.es/etraffic/ShareAjax?accion=getRoad4Provincia&codProv={}"
output_file = "roads.json"

# Container for the roads to be read
roads = {}

# Read the provinces from the JSON
provinces = data.getProvinces()

# For each province, load the associated roads
for province in provinces:
    try:
        response = requests.get(base_url.format(province["code_number"]))
        roads[province["code_number"]] = response.json()
        print u"{} roads for province '{}'".format(len(roads[province["code_number"]]), province["pretty_name"])

    except KeyError:
        print u"Woops, looks like the province '{}' has no code_number".format(province["pretty_name"])

# Write the results to the file
with io.open(output_file, "w", encoding='utf8') as the_file:
    the_file.write(json.dumps(roads, indent=2, ensure_ascii=False))

num_roads = sum(len(x) for x in roads.values())
print "{} roads written to {}".format(num_roads, output_file)