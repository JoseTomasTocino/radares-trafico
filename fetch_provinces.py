#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
import pprint
import io
from bs4 import BeautifulSoup
from util import levenshtein

base_url = "http://www.dgt.es/es/el-trafico/control-de-velocidad/index-radares.shtml"
etraffic_url = "http://infocar.dgt.es/etraffic"
output_file = "provinces.json"

# Container for the provinces
provinces = []

# Get the web content
response = requests.get(base_url)

# Build the soup
soup = BeautifulSoup(response.content)

# Find the container by its header
container = soup.select("#dgt-trafico")[0].parent

# Find the links
links = container.select('ul li a[href^="/es"]')

# For each link, get the pretty province name and the codified name
for link in links:
    pretty_name = link.text
    code_name = [x for x in link['href'].split("/") if x][-1]

    provinces.append({'pretty_name' : pretty_name, "code_name" : code_name})

# In the eTraffic website, let's get the codes for each province
soup = BeautifulSoup(requests.get(etraffic_url).content)

# Container for the codes
codes = {}

# The list of provinces has the id #provincia
for element in soup.select("#provincia option"):
    codes[element.text] = element["value"]

# Now, let's match the provinces with the codes
for province in provinces:

    matching_code = None

    # Go over all the recorded codes
    for current_name, current_code in codes.items():

        # If there's a direct match
        if province["pretty_name"].lower() in current_name.lower():
            matching_code = current_code
            break

    # If no matching code has been found, try to find the most similar province name
    # using levenshtein distance

    if not matching_code:
        min_val = len(current_name) * 2

        for current_name, current_code in codes.items():
            cur_val = levenshtein(province["pretty_name"].lower(), current_name.lower())

            if min_val > cur_val:
                min_val = cur_val
                matching_code = current_code

    province["code_number"] = matching_code

# Write the results to the file
with io.open(output_file, "w", encoding='utf8') as the_file:
    the_file.write(json.dumps(provinces, indent=2, ensure_ascii=False))

print "{} provinces written to {}".format(len(provinces), output_file)