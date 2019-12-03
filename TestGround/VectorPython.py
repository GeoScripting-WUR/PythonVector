#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Geoscripting 2020
Lesson 11 - Python Vector
v20191203
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
gs.crs = {'init': 'epsg:28992'}
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
wageningenGDF = gpd.GeoDataFrame(df, geometry=geometry)
wageningenGDF.crs = {'init': 'epsg:28992'}
wageningenGDF.plot(marker='*', color='green', markersize=50)
print(type(wageningenGDF), len(wageningenGDF))

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="specify_random_user_agent")
location = geolocator.geocode("Wageningen University")
print((location.latitude, location.longitude))
# It should print two coordinates: (lat: 51.98527485, lon:5.66370505205543)

from pyproj import Proj, transform
geolocator = Nominatim(user_agent="specify_random_user_agent")
location = geolocator.geocode("Wageningen University")
inProj = Proj(init='epsg:4326') #WGS84
outProj = Proj(init='epsg:28992') #RD New
x, y = transform(inProj, outProj, location.longitude, location.latitude)
print([x, y])

data = {'name': ['a', 'b', 'c'],
        'x': [173994.1578792833, 173974.1578792833, 173910.1578792833],
        'y': [444135.6032947102, 444186.6032947102, 444111.6032947102]}
df = pd.DataFrame(data)
geometry = [Point(xy) for xy in zip(df['x'], df['y'])]
wageningenGDF = gpd.GeoDataFrame(df, geometry=geometry)
print(wageningenGDF.crs)
wageningenGDF.crs = {'init': 'epsg:28992'}
print(wageningenGDF.crs)
wageningenGDF = wageningenGDF.to_crs({'init': 'epsg:4326'})
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

WfsUrl = 'https://geodata.nationaalgeoregister.nl/bag/wfs?'
wfs = WebFeatureService(url=WfsUrl, version='2.0.0')
layer = list(wfs.contents)[1]
xmin, xmax, ymin, ymax = x-1000, x+1000, y-1000, y+1000
response = wfs.getfeature(typename=layer, bbox=(xmin, ymin, xmax, ymax), outputFormat='application/gml+xml; version=3.2')
with open('./data/Buildings.gml', 'w') as file:
    file.write(response.read())
BuildingsGDF = gpd.read_file('./data/Buildings.gml')
print(type(BuildingsGDF))
roadlayer = roadsGDF.plot(color='grey')
roadlayer.set_xlim(xmin, xmax)
roadlayer.set_ylim(ymin, ymax)
BuildingsGDF.plot(ax=roadlayer, color='red')
plt.savefig('./output/BuildingsAndRoads.png')

parcelsWFSUrl = 'https://geodata.nationaalgeoregister.nl/kadastralekaartv3/wfs'
parcelsWFS = WebFeatureService(url=parcelsWFSUrl, version='2.0.0')
print(list(parcelsWFS.contents))
xmin, xmax, ymin, ymax = x-500, x+500, y-500, y+500
responseParcels = parcelsWFS.getfeature(typename='kadastralekaartv3:perceel', 
                                        bbox=(xmin, ymin, xmax, ymax), 
                                        maxfeatures=100, outputFormat='json', startindex=0)
data = json.loads(responseParcels.read())
parcelsGDF = gpd.GeoDataFrame.from_features(data['features'])
parcelsGDF.plot()
plt.savefig('./output/ParcelsGDF.png')

print(parcelsGDF.columns)
print(parcelsGDF.head())
print(parcelsGDF.area)

print(parcelsGDF.area > 100000)
largeParcelsGDF = parcelsGDF.loc[parcelsGDF.area > 100000, :]
largeParcelsGDF.plot()

print(parcelsGDF['perceelnummer'])

print(parcelsGDF['perceelnummer'].isin(['11185', '11593']))
campusParcelsGDF = parcelsGDF[parcelsGDF['perceelnummer'].isin(['11185', '11725'])]

campusParcelsGDF.plot()
plt.savefig('./output/CampusParcels.png')

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

print(type(largeParcelsGDF))
print(type(largeParcelsGDF.geometry))
print(type(largeParcelsGDF['geometry']))

parcelsUnionGS = gpd.GeoSeries(largeParcelsGDF.unary_union)
parcelsUnionGS.plot()

parcelsConvexGDF = gpd.GeoDataFrame(parcelsUnionGS.convex_hull)
parcelsConvexGDF = parcelsConvexGDF.rename(columns={0:'geometry'}).set_geometry('geometry')
parcelsConvexGDF.plot()

# we need polygons instead of line features for the overlay
RoadsPolygonGDF = gpd.GeoDataFrame(roadsGDF, geometry=roadsGDF.buffer(distance=5))
RoadsPolygonGDF.plot()
# perform an intersection overlay
roadsIntersectionGDF = gpd.overlay(parcelsConvexGDF, RoadsPolygonGDF, how="intersection")
roadsIntersectionGDF.plot()
plt.savefig('./output/roadsIntersectionGDF.png')

WageningenRoadsGDF = RoadsPolygonGDF.loc[RoadsPolygonGDF['gme_naam']=='Wageningen']
print(sum(WageningenRoadsGDF.area))
WageningenRoadsGDF.plot()
plt.savefig('./output/WageningenRoadsGDF.png')

import folium
campusMap = folium.Map([location.latitude, location.longitude], zoom_start=17)
BuildingsGDF.crs = {'init': 'epsg:28992'}
BuildingsGDF.to_crs({'init': 'epsg:4326'})
RoadsPolygonGDF.crs = {'init': 'epsg:28992'}
RoadsPolygonGDF.to_crs({'init': 'epsg:4326'})
campusMap.choropleth(BuildingsGDF, name='Building construction years', 
                     data=BuildingsGDF, columns=['gml_id', 'bouwjaar'], 
                     key_on='feature.properties.gml_id', fill_color='RdYlGn',
                     fill_opacity=0.7, line_opacity=0.2,legend_name='Construction year')
campusMap.choropleth(RoadsPolygonGDF)
folium.LayerControl().add_to(campusMap)
campusMap.save('./output/campusMap.html')
campusMap

## check code critically, we request from wfs without storing a gml file!
import geopandas as gpd
from requests import Request
from owslib.wfs import WebFeatureService
from matplotlib import pyplot as plt
# extract only buildings on and around WUR campus
url = 'https://geodata.nationaalgeoregister.nl/bag/wfs'
layer = 'bag:pand'
# speciy the boundary box for extracting
xmin, xmax, ymin, ymax = x-300, x+600, y-300, y+300
bb = (xmin, ymin, xmax, ymax)
bb = ','.join(map(str, bb)) # string needed for the request
# Specify the parameters for fetching the data
params = dict(service='WFS', version="2.0.0", request='GetFeature',
      typeName=layer, outputFormat='text/xml; subtype=gml/3.2',
      srsname='urn:ogc:def:crs:EPSG::28992', bbox=bb)
# Parse the URL with parameters
q = Request('GET', url, params=params).prepare().url
# Read data from URL
BuildingsGDF = gpd.read_file(q)


#
#WfsUrl = 'https://geodata.nationaalgeoregister.nl/bag/wfs?'
#wfs = WebFeatureService(url=WfsUrl, version='2.0.0')
#layer = list(wfs.contents)[1]
#xmin, xmax, ymin, ymax = x-300, x+600, y-300, y+300
#response = wfs.getfeature(typename=layer, bbox=(xmin, ymin, xmax, ymax), outputFormat='application/gml+xml; version=3.2')
#with open('./data/WURBuildings.gml', 'w') as file:
#    file.write(response.read())
#BuildingsGDF = gpd.read_file('./data/WURBuildings.gml')

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
city = ox.gdf_from_place('Wageningen, Netherlands')
ox.plot_shape(ox.project_gdf(city))
WageningenRoadsGraph = ox.graph_from_place('Wageningen, Netherlands', network_type='all')
ox.plot_graph(WageningenRoadsGraph, fig_height=20, fig_width=20)
ox.save_graph_shapefile(G=WageningenRoadsGraph, filename='OSMnetwork_Wageningen.shp')
gdf_nodes, gdf_edges = ox.graph_to_gdfs(G=WageningenRoadsGraph)
print(gdf_nodes.info())
print(gdf_edges.info())

source = ox.get_nearest_node(WageningenRoadsGraph, (51.987817, 5.665779))
target = ox.get_nearest_node(WageningenRoadsGraph, (51.964870, 5.662409))
shortestroute = ox.nx.shortest_path(G=WageningenRoadsGraph, 
                                    source=source, target=target, weight='length')
ox.plot_graph_route(WageningenRoadsGraph, shortestroute, 
                    fig_height=20, fig_width=20)

#
#
###
#import osmnx as ox
#city = ox.gdf_from_place('Wageningen University')
#ox.plot_shape(ox.project_gdf(city))
#city = ox.gdf_from_place('Dreijen')
#ox.plot_shape(ox.project_gdf(city))
#WageningenRoadsGraph = ox.graph_from_place('Dreijenplein', network_type='all')
#ox.plot_graph(WageningenRoadsGraph, fig_height=10, fig_width=10)
#ox.save_graph_shapefile(G=WageningenRoadsGraph, filename='OSMnetwork_Wageningen.shp')
#gdf_nodes, gdf_edges = ox.graph_to_gdfs(G=WageningenRoadsGraph)
#print(gdf_nodes.info())
#print(gdf_edges.info())


