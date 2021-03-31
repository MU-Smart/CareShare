import matplotlib.pyplot as plt
import geojson
import math
import numpy as np
import requests
from column_remap import remap
from sklearn.cluster import KMeans
import imp

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


plt.plot(y_coordinates,x_coordinates)


import pandas as pd
import os

df = pd.read_csv("./chicago_taxi_trips_2016_12.csv",nrows=5000)
    
lat = []
lon = []
for i,row in df.iterrows():
    '''
    '''
    try:
        if(row["pickup_latitude"]!='nan' and row["pickup_latitude"]!='NaN'):
            
            lat.append(remap(row["pickup_latitude"],"pickup_latitude"))
            lon.append(remap(row["pickup_longitude"],"pickup_longitude"))
    except ValueError:
        continue


cordinates = np.vstack((lon, lat)).T
kmeans_main = KMeans(n_clusters=15).fit(cordinates)
centers_main = np.array(kmeans_main.cluster_centers_)
np.save("request.npy", centers_main)

x = [i[0] for i in centers_main]
y = [i[1] for i in centers_main]

plt.scatter(x,y,color="red")
plt.show()
