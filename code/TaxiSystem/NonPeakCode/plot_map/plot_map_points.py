import matplotlib.pyplot as plt
import geojson
import math
import numpy as np
import requests
from column_remap import remap

radius_earth = 6371000
with open("Boundaries - City.geojson") as f:
    gj = geojson.load(f)
features = gj['features'][0]
coordinates = features["geometry"]["coordinates"]
x_coordinates = []
y_coordinates = []
for i in coordinates:
    for j in i:
        for k in j:
            x_coordinates.append(k[1])
            y_coordinates.append(k[0])
        break


#print(len(x_coordinates),max(x_coordinates),min(x_coordinates))
#print(len(y_coordinates),max(y_coordinates),min(y_coordinates))


plt.plot(y_coordinates,x_coordinates)


import pandas as pd
import os

df = pd.read_csv("../chicago_taxi_trips_2016_12.csv",nrows=500)
    
lat = []
lon = []
for i,row in df.iterrows():
    '''
    '''
    try:
        if(row["pickup_latitude"]!='nan' and row["pickup_latitude"]!='NaN'):
            #print(remap(row["pickup_latitude"],"pickup_latitude"))
            lat.append(remap(row["pickup_latitude"],"pickup_latitude"))
            lon.append(remap(row["pickup_longitude"],"pickup_longitude"))
    except ValueError:
        continue
    
plt.scatter(lon,lat,color="red")
plt.savefig("map")
