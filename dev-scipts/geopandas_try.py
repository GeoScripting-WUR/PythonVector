#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 11:29:44 2024

@author: osboxes
"""


from owslib.wfs import WebFeatureService
import geopandas as gpd
import json 
from geodatasets import data 
import geodatasets
import matplotlib.pyplot as plt

import cartopy.crs as ccrs
import cartopy.feature as cfeature


# Define center point and create bbox for study area
x, y = (173994.1578792833, 444133.60329471016)
xmin, xmax, ymin, ymax = x - 500, x + 500, y - 500, y + 500

# Get the WFS of the BAG
wfsUrl = 'https://service.pdok.nl/lv/bag/wfs/v2_0'
wfs = WebFeatureService(url=wfsUrl, version='2.0.0')
layer = list(wfs.contents)[0]
# Get the features for the study area
# notice that we now get them as json, in contrast to before
response = wfs.getfeature(typename=layer, bbox=(xmin, ymin, xmax, ymax), outputFormat='json')
data = json.loads(response.read())

# Create GeoDataFrame, without saving first
buildingsGDF = gpd.GeoDataFrame.from_features(data['features'])
buildingsGDF.crs=28992



####################3

epsg = 3034

# riversGDF = gpd.read_file(geodatasets.get_path('eea.large_rivers'))
# riversGDF = riversGDF.to_crs(epsg)

# fig = plt.figure(figsize=(11, 8.5))
# projEU = ccrs.epsg(epsg)
# ax = plt.subplot(1, 1, 1, projection=projEU)
# ax.set_extent(riversGDF.total_bounds, crs=projEU)


# ax.set_title("Lambert Azimuthal Equal Area Projection")
# ax.coastlines(linewidth=0.5)

# riversGDF.plot(ax=ax, color='blue', linewidth=1)


buildings_3857 = buildingsGDF.to_crs(epsg)

fig = plt.figure(figsize=(11, 8.5))
projEU = ccrs.epsg(epsg)

nax = plt.subplot(1, 1, 1, projection=projEU)

# nax.set_extent(buildings_3857.total_bounds, crs=projEU)

building_axes = buildings_3857.plot(ax=nax, crs=projEU)
# riversbufferGDF = gpd.GeoDataFrame(riversGDF, geometry=riversGDF.buffer(distance=10000)) 

# riversbufferGDF.plot(ax=ax, facecolor = 'blue')
