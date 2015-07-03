#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import json
import itertools

from util import levenshtein

provinces = None
roads = None

def getProvinces(province_file="provinces.json"):
    if "data" not in getProvinces.__dict__:
        with io.open(province_file, 'r', encoding='utf8') as f:
            getProvinces.data = json.load(f)

    return getProvinces.data

def getRoads(road_file="roads.json"):
    if "data" not in getRoads.__dict__:
        with io.open(road_file, 'r', encoding='utf8') as f:
            getRoads.data = json.load(f)

    return getRoads.data

def getCodeNumberForProvince(province):

    # Bind the first argument
    lv = lambda x: levenshtein(province.lower(), x.lower())

    provinces = getProvinces()

    # Apply the levenshtein distance to all the province names
    computed = [(x['code_number'], lv(x['pretty_name'])) for x in provinces]

    # Return the code for the most similar one (lowest levenshtein distance)
    return min(computed, key=lambda x:x[1])[0]

def getCodeNumberForRoad(road, province_code):
    roads = getRoads()

    # Get the matching road
    z = [x for x in roads[province_code] if x["carrNombre"] == road]

    if z:
        return z[0]["carrCodigo"]
    else:
        return None


if __name__ == '__main__':
    print getCodeNumberForRoad("N-443")
