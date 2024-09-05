#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 15:16:40 2024

@author: osboxes
"""

from owslib.wfs import WebFeatureService
import geopandas as gpd
import matplotlib.pyplot as plt

''' 
# Put the WFS url in a variable
wfsUrl = 'https://service.pdok.nl/cbs/postcode6/2022/wfs/v1_0?request=GetCapabilities&service=WFS'

# Create a WFS object
wfs = WebFeatureService(url=wfsUrl, version='2.0.0')

# Get the title from the object
print(wfs.identification.title)

# Check the contents of the WFS
print(list(wfs.contents))

# Define center point and create bbox for study area
x, y = (173994.1578792833, 444133.60329471016)
xmin, xmax, ymin, ymax = x - 1000, x + 350, y - 1000, y + 350

# Get the features for the study area (using the wfs from the previous code block)
response = wfs.getfeature(typename=list(wfs.contents)[0], bbox=(xmin, ymin, xmax, ymax))

# Save them to disk
with open('data/postal_codes.gml', 'wb') as file:
    file.write(response.read())

# Read in again with GeoPandas
pc_gdf = gpd.read_file('data/postal_codes.gml')

# Inspect and plot to get a quick view
print(type(pc_gdf))
pc_gdf.plot()
plt.show()


import json

# Get the WFS of the BAG
wfsUrl = 'https://service.pdok.nl/lv/bag/wfs/v2_0'
wfs = WebFeatureService(url=wfsUrl, version='2.0.0')
layer = list(wfs.contents)[0]

# Define center point and create bbox for study area
x, y = (173994.1578792833, 444133.60329471016)
xmin, xmax, ymin, ymax = x - 500, x + 500, y - 500, y + 500

# Get the features for the study area
# notice that we now get them as json, in contrast to before
response = wfs.getfeature(typename=layer, bbox=(xmin, ymin, xmax, ymax), outputFormat='json')
data = json.loads(response.read())

# Create GeoDataFrame, without saving first
buildingsGDF = gpd.GeoDataFrame.from_features(data['features'])

# Set crs to RD New
buildingsGDF.crs = 28992

# Plot roads and buildings together
pc_layer = pc_gdf.plot(color='grey')
buildingsGDF.plot(ax=pc_layer, color='red')

# Set the limits of the x and y axis
pc_layer.set_xlim(xmin, xmax)
pc_layer.set_ylim(ymin, ymax)

# Save the figure to disk
plt.savefig('./output/postalcoades_roads.png')



# Pandas function that returns the column labels of the DataFrame
print(buildingsGDF.columns)

# Pandas function that returns the first n rows, default n = 5
print(buildingsGDF.head())

# shape area (in the units of the projection)
print(buildingsGDF.area)

# Inspect first
print(buildingsGDF.area > 1000)

# Make the selection, select all rows with area > 1000 m2, and all columns
# Using 'label based' indexing with loc, here with a Boolean array
largeBuildingsGDF = buildingsGDF.loc[buildingsGDF.area > 1000, :]

# Plot
largeBuildingsGDF.plot()
''' 

import json 

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
# Set crs to RD New
buildingsGDF.crs = 28992
# Inspect first
print( buildingsGDF['status'] != 'Pand in gebruik' )

# Make the selection, the list of required values can contain more than one item
newBuildingsGDF = buildingsGDF[buildingsGDF['status'] != 'Pand in gebruik']

# Plot the new buildings with a basemap for reference
# based on https://geopandas.org/gallery/plotting_basemap_background.html
import contextily as ctx

# Re-project
newBuildingsGDF = newBuildingsGDF.to_crs(epsg=3857)

# Plot with 50% transparency
ax = newBuildingsGDF.plot(figsize=(10, 10), alpha=0.5, edgecolor='k')
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=17)
ax.set_axis_off()