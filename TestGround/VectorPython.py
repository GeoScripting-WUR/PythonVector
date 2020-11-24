#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Geoscripting 2020
Lesson 10 - Python Vector
v20201124
CHappyhill
"""
import os
if not os.path.exists('data'): os.makedirs('data')
if not os.path.exists('output'): os.makedirs('output')

import matplotlib.pyplot as plt
#
#import os
#os.getcwd()

from shapely.geometry import Point
import geopandas as gpd
wageningenCampus = Point([173994.1578792833, 444133.60329471016])
print(type(wageningenCampus))
gs = gpd.GeoSeries([wageningenCampus])
print(type(gs), len(gs))

from shapely.wkt import loads
WKTstring = 'POINT(173994.1578792833 444133.6032947102)'
gs = gpd.GeoSeries([loads(WKTstring)])
gs.crs = "EPSG:28992" # specify manually the projection
gsBuffer = gs.buffer(100)
print(gs.geometry)
print(gsBuffer.geometry)

import pandas as pd
data = {'name': ['a', 'b', 'c'],
        'x': [173994.1578792833, 173974.1578792833, 173910.1578792833],
        'y': [444135.6032947102, 444186.6032947102, 444111.6032947102]}
df = pd.DataFrame(data)
print(df.head)

geometry = [Point(xy) for xy in zip(df['x'], df['y'])]
wageningenGDF = gpd.GeoDataFrame(df, geometry=geometry, crs = "EPSG:28992") # note that we here specify the CRS (projection) directly while reading to GDF
wageningenGDF.plot(marker='*', color='green', markersize=50)
print(type(wageningenGDF), len(wageningenGDF))

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="specify_random_user_agent")
location = geolocator.geocode("Wageningen University")
print((location.latitude, location.longitude))
# It should print two coordinates: (lat: 51.98527485, lon:5.66370505205543)

from pyproj import Transformer
geolocator = Nominatim(user_agent="specify_random_user_agent")
location = geolocator.geocode("Wageningen University")
x, y = Transformer.from_crs(4326, 28992).transform(location.latitude, location.longitude) #mind swap in axis order! 
print([x, y]) # always inspect results of your data handling, in this case double-check the coordinates due to potential swap in axis order.

data = {'name': ['a', 'b', 'c'],
        'x': [173994.1578792833, 173974.1578792833, 173910.1578792833],
        'y': [444135.6032947102, 444186.6032947102, 444111.6032947102]}
df = pd.DataFrame(data)
geometry = [Point(xy) for xy in zip(df['x'], df['y'])]
wageningenGDF = gpd.GeoDataFrame(df, geometry=geometry)
print(wageningenGDF.crs)
wageningenGDF.crs = 'EPSG:28992'
print(wageningenGDF.crs)
wageningenGDF = wageningenGDF.to_crs('EPSG:4326')
print(wageningenGDF.crs)

import fiona
print(fiona.supported_drivers)

data = {'name': ['a', 'b', 'c'],
        'x': [173994.1578792833, 173974.1578792833, 173910.1578792833],
        'y': [444135.6032947102, 444186.6032947102, 444111.6032947102]}
df = pd.DataFrame(data)
geometry = [Point(xy) for xy in zip(df['x'], df['y'])]
wageningenGDF = gpd.GeoDataFrame(df, geometry=geometry)
wageningenGDF.to_file(filename='./data/wageningenPOI.geojson', driver='GeoJSON')
wageningenGDF.to_file(filename='./data/wageningenPOI.shp', driver='ESRI Shapefile')

jsonGDF = gpd.read_file('./data/wageningenPOI.geojson')
shpGDF = gpd.read_file('./data/wageningenPOI.shp')

from owslib.wfs import WebFeatureService
WfsUrl = 'https://geodata.nationaalgeoregister.nl/nwbwegen/wfs?'
wfs = WebFeatureService(url=WfsUrl, version='2.0.0')
wfs.identification.title
print(list(wfs.contents))

import json
# x, y = (173994.1578792833, 444133.60329471016) #uncomment if you lost x, y coordinates or Nominatim didn't work above :D
WfsUrl = 'https://geodata.nationaalgeoregister.nl/nwbwegen/wfs?'
wfs = WebFeatureService(url=WfsUrl, version='2.0.0')
layer = list(wfs.contents)[0]
xmin, xmax, ymin, ymax = x-2000, x+2000, y-2000, y+2000
response = wfs.getfeature(typename=layer, bbox=(xmin, ymin, xmax, ymax), outputFormat='application/gml+xml; version=3.2')
with open('./data/Roads.gml', 'wb') as file:
    file.write(response.read())
roadsGDF = gpd.read_file('./data/Roads.gml')
print(type(roadsGDF))
roadsGDF.plot()
plt.savefig('./output/RoadsGDF.png')

len(roadsGDF)
roadsGDF.info()

WfsUrl = 'https://geodata.nationaalgeoregister.nl/bag/wfs/v1_1'
wfs = WebFeatureService(url=WfsUrl, version='1.1.0')
layer = list(wfs.contents)[1]
xmin, xmax, ymin, ymax = x-500, x+500, y-500, y+500
response = wfs.getfeature(typename=layer, bbox=(xmin, ymin, xmax, ymax), outputFormat='json')
data = json.loads(response.read())
BuildingsGDF = gpd.GeoDataFrame.from_features(data['features'], crs=28992)
print(type(BuildingsGDF))
roadlayer = roadsGDF.plot(color='grey')
roadlayer.set_xlim(xmin, xmax)
roadlayer.set_ylim(ymin, ymax)
BuildingsGDF.plot(ax=roadlayer, color='red')
plt.savefig('./output/BuildingsAndRoads.png')

#parcelsWFSUrl = 'https://geodata.nationaalgeoregister.nl/kadastralekaart/wfs/v4_0?service=WFS'
#parcelsWFS = WebFeatureService(url=parcelsWFSUrl)
#print(list(parcelsWFS.contents))
#xmin, xmax, ymin, ymax = x-500, x+500, y-500, y+500
#responseParcels = parcelsWFS.getfeature(typename='perceel', 
#                                        bbox=(xmin, ymin, xmax, ymax), 
#                                        maxfeatures=100, outputFormat='json', startindex=0)
#data = json.loads(responseParcels.read())
#parcelsGDF = gpd.GeoDataFrame.from_features(data['features'])
#parcelsGDF.plot()
#plt.savefig('./output/ParcelsGDF.png')

print(BuildingsGDF.columns)
print(BuildingsGDF.head())
print(BuildingsGDF.area)

print(BuildingsGDF.area > 1000)
largeBuildingsGDF = BuildingsGDF.loc[BuildingsGDF.area > 1000, :]
largeBuildingsGDF.plot()

print(BuildingsGDF['bouwjaar'])

print(BuildingsGDF['status'].isin(['Bouw gestart']))
NewBuildingsGDF = BuildingsGDF[BuildingsGDF['status'].isin(['Bouw gestart'])]

## plot the new buildings with a basemap for reference
## based on https://geopandas.org/gallery/plotting_basemap_background.html
import contextily as ctx
NewBuildingsGDF = NewBuildingsGDF.to_crs(epsg=3857)
ax = NewBuildingsGDF.plot(figsize=(10, 5), alpha=0.5, edgecolor='k')
ctx.add_basemap(ax, source=ctx.providers.Stamen.TonerLite)
ax.set_axis_off()
plt.savefig('./output/NewBuildings.png')

##
#c = parcelsGDF
#c['coords'] = c['geometry'].apply(lambda x: x.representative_point().coords[:])
#c['coords'] = [coords[0] for coords in c['coords']]
#c.plot(figsize=(20,10))
#for idx, row in c.iterrows():
#    plt.annotate(s=row['perceelnummer'], xy=row['coords'],
#                 horizontalalignment='center')
#
#['10709', '10905', '10906', '10907', '10908', '10909', '11184', '11185', '11208', '11593']
#perceelnummers = ['11175', '11185', '11725', '11077', '11183']
#campusParcelsGDF = parcelsGDF[parcelsGDF['perceelnummer'].isin(perceelnummers)]
#
#parcelsConvexGDF = gpd.GeoDataFrame(campusParcelsGDF.unary_union)
#parcelsConvexGDF = parcelsConvexGDF.rename(columns={0:'geometry'}).set_geometry('geometry')
#parcelsConvexGDF.plot()
#parcelsConvexGDF = gpd.GeoDataFrame(parcelsConvexGDF.convex_hull)
#parcelsConvexGDF = parcelsConvexGDF.rename(columns={0:'geometry'}).set_geometry('geometry')
#parcelsConvexGDF.plot()
#
##
#roadlayer = roadsGDF.plot(color='grey')
#campusParcelsGDF.plot(ax=roadlayer, color='red')
#

print(type(roadsGDF))
print(type(roadsGDF.geometry))
print(roadsGDF['geometry'])

RoadsPolygonGDF = gpd.GeoDataFrame(roadsGDF, geometry=roadsGDF.buffer(distance=1.5)) # buffer of 1.5 m on both sides
RoadsPolygonGDF.plot(color='blue', edgecolor='blue')
RoadsPolygonGDF.area.sum()

RoadsUnionGS = gpd.GeoSeries(RoadsPolygonGDF.unary_union)
RoadsUnionGS.area
print('There was an overlap of ' + round((RoadsPolygonGDF.area.sum() - RoadsUnionGS.area[0]), 1).astype(str) + ' meters.')

NewBuildingsGDF = NewBuildingsGDF.to_crs(epsg=28992)
AreaOfInterestGS = gpd.GeoSeries(NewBuildingsGDF.buffer(distance=100).unary_union)
AreaOfInterestGDF = gpd.GeoDataFrame(AreaOfInterestGS.convex_hull)
AreaOfInterestGDF = AreaOfInterestGDF.rename(columns={0:'geometry'}).set_geometry('geometry')
AreaOfInterestGDF.crs = 'EPSG:28992' 
#AreaOfInterestGDF.plot()
## perform an intersection overlay
roadsIntersectionGDF = gpd.overlay(AreaOfInterestGDF, RoadsPolygonGDF, how="intersection")
#roadsIntersectionGDF.plot(color='blue', edgecolor='blue')
## plot the results 
roadlayer = roadsIntersectionGDF.plot(color='grey', edgecolor='grey')
roadlayer.set_xlim(xmin, xmax)
roadlayer.set_ylim(ymin, ymax)
NewBuildingsGDF.plot(ax=roadlayer, color='red')
plt.savefig('./output/roadsIntersectionGDF.png')

WageningenRoadsGDF = RoadsPolygonGDF.loc[RoadsPolygonGDF['gme_naam']=='Wageningen']
print(sum(WageningenRoadsGDF.area))
WageningenRoadsGDF.plot(edgecolor='purple')
plt.savefig('./output/WageningenRoadsGDF.png')

import folium
campusMap = folium.Map([location.latitude, location.longitude], zoom_start=17)
BuildingsGDF = BuildingsGDF.to_crs(4326)
RoadsPolygonGDF = RoadsPolygonGDF.to_crs(4326)
campusMap.choropleth(BuildingsGDF, name='Building construction years', 
                     data=BuildingsGDF, columns=['gid', 'bouwjaar'], 
                     key_on='feature.properties.gid', fill_color='RdYlGn',
                     fill_opacity=0.7, line_opacity=0.2,legend_name='Construction year')
campusMap.choropleth(RoadsPolygonGDF, name='Roads')
folium.LayerControl().add_to(campusMap)
campusMap.save('./output/campusMap.html')
campusMap

import geopandas as gpd
from requests import Request
from owslib.wfs import WebFeatureService
from matplotlib import pyplot as plt
# extract only buildings on and around WUR campus
WfsUrl = 'https://geodata.nationaalgeoregister.nl/bag/wfs/v1_1'
wfs = WebFeatureService(url=WfsUrl, version='1.1.0')
layer = list(wfs.contents)[1]
xmin, xmax, ymin, ymax = x-300, x+600, y-300, y+300
response = wfs.getfeature(typename=layer, bbox=(xmin, ymin, xmax, ymax), outputFormat='json')
data = json.loads(response.read())
BuildingsGDF = gpd.GeoDataFrame.from_features(data['features'], crs=28992)
# create visualisation
f, ax = plt.subplots(1, figsize=(10, 5))
ax.set_title('WUR campus buildings')
ax.set_facecolor("grey")
roadlayer = RoadsPolygonGDF.plot(ax=ax, legend=True)
roadlayer.set_xlim(xmin, xmax)
roadlayer.set_ylim(ymin, ymax)
buildingslayer = BuildingsGDF.plot(ax=roadlayer, column='bouwjaar', 
                                   cmap='brg', #see https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html
                                   legend=True, 
                                   legend_kwds={'label': "Construction year",'orientation': "vertical"})
plt.savefig('./output/WURcampusMapBuildings.png')

import osmnx as ox
city = ox.geocoder.geocode_to_gdf('Wageningen, Netherlands')
ox.plot.plot_footprints(ox.project_gdf(city))
WageningenRoadsGraph = ox.graph.graph_from_place('Wageningen, Netherlands', network_type='bike')
ox.plot.plot_graph(WageningenRoadsGraph, figsize=(10,10), node_size=2)
ox.io.save_graph_shapefile(G=WageningenRoadsGraph, filepath='OSMnetwork_Wageningen.shp')
gdf_nodes, gdf_edges = ox.graph_to_gdfs(G=WageningenRoadsGraph)
print(gdf_nodes.info())
print(gdf_edges.info())

source = ox.distance.get_nearest_node(WageningenRoadsGraph, (51.987817, 5.665779))
target = ox.distance.get_nearest_node(WageningenRoadsGraph, (51.964870, 5.662409))
shortestroute = ox.distance.shortest_path(G=WageningenRoadsGraph, 
                                    orig=source, dest=target, weight='length')
ox.plot.plot_graph_route(WageningenRoadsGraph, shortestroute, figsize=(20,20),
                         route_alpha=0.6, route_color='darkred', 
                         route_linewidth=10, orig_dest_size=100)



