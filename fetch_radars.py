#!/usr/bin/env python
# coding: utf-8

import sys
import io
import json
import requests
from bs4 import BeautifulSoup

import data

current_city = "cadiz"
output_file = "radars.json"

base_url = "http://www.dgt.es/es/el-trafico/control-de-velocidad/"
base_gps_url = "http://infocar.dgt.es/etraffic/BuscarElementos?accion=centrar&provincia={}&codCarretera={}&PK={}"
current_page = 1

roads = data.getRoads()
provinces = data.getProvinces()

# Builds the url for the current city and page number
get_current_url = lambda: base_url + current_city + "/" + ("index.shtml" if current_page == 1 else "index-paginacion-" + "%03d" % current_page + ".shtml")

# Get the initial URL
current_url = get_current_url()

# Get the initial contents
current_content = requests.get(current_url)

# Build the soup and get the number of radars and pages
soup = BeautifulSoup(current_content.text)
num_results = int(soup.select("nav.xpg.lfd p strong")[0].string)
num_pages = int(soup.select("nav.xpg.lfd div dl dd")[2].string)

final_radars = []

while current_page <= num_pages:
    # Build the URL and get the content for the current page
    current_url = get_current_url()
    current_content = requests.get(current_url)

    # Build the soup
    soup = BeautifulSoup(current_content.text)

    print "-----------------------"
    print "Radares de la página {}".format(current_page)

    # Fetch the radars for the current page
    radars = soup.select("table.tb2 tbody tr")

    # Iterate over the radars
    for radar in radars:
        try:
            road, province, kind, km, direction = [x.string for x in radar.find_all("td")]
            road = ' '.join(road.strip().split())
            province = ' '.join(province.strip().split())
            kind = ' '.join(kind.strip().split())
            km = ' '.join(km.strip().split())
            direction = ' '.join(direction.strip().split())

            # Get the code for the province
            province_code = data.getCodeNumberForProvince(province)

            # Get the code for the road
            road_code = data.getCodeNumberForRoad(road, province_code)

            # If it's a fixed radar, there's just one km point
            if '-' not in km:
                kms = [float(km)]

            # Otherwise, the radar can be placed anywhere in the given interval,
            # so we'll plot points every five kilometers
            else:
                km_begin, km_end = [float(x.strip()) for x in km.split("-")]
                num_mid_points = int((km_end - km_begin) / 2.0)
                kms = [km_begin] + [km_begin + (km_end - km_begin) / num_mid_points * i for i in range(1, num_mid_points)] + [km_end]

            kms_gps = []

            # Get the GPS coordinates using a request for each km point
            for km in kms:
                response = requests.get(base_gps_url.format(province_code, road_code, km)).json()
                kms_gps.append({ "lng": float(response["lng"]), "lat": float(response["lat"]) })

            the_radar = {
                "road": road,
                "road_code": road_code,
                "province": province,
                "province_code": province_code,
                "kind": kind,
                "direction": direction,
                "kms": kms,
                "kms_gps": kms_gps
            }

            final_radars.append(the_radar)

            print road, province, kind, kms, kms_gps, direction, province_code, road_code

        except:
            # Yeah baby that's how I roll
            continue

    # Get the next current page number
    current_page += 1

# Write the results to the file
with io.open(output_file, "w", encoding='utf8') as the_file:
    the_file.write(json.dumps(final_radars, indent=2, ensure_ascii=False))

print "{} radars written to {}".format(len(final_radars), output_file)