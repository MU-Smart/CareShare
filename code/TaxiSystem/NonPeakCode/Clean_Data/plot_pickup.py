# -*- coding: utf-8 -*-
"""
Created on Mon Dec 31 08:06:37 2018

@author: Aishwarya
"""

import pandas as pd
import json
import matplotlib.pyplot as plt
import geojson

with open("./Extra_Chicago2016/column_remapping.json") as f:
    mapping = json.load(f)

#df = pd.read_csv("./chicago_taxi_trips_2016_12_clean_companywise_randomtime.csv")
pass_df = pd.read_csv("./1hour_7_8_passenger.csv")
taxi_df = pd.read_csv("./1hour_7_8_taxis.csv")

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


pickup_lat = []
pickup_lon = []

for i,row in pass_df.iterrows():
    '''
    pickup_lat.append(float(mapping["pickup_latitude"][str(int(row["pickup_latitude"]))]))
    pickup_lon.append(float(mapping["pickup_longitude"][str(int(row["pickup_longitude"]))]))
    '''
    pickup_lat.append(row["pickup_latitude"])
    pickup_lon.append(row["pickup_longitude"])
    
plt.scatter(pickup_lon,pickup_lat,color="red")

taxi_lat = []
taxi_lon = []

for i,row in taxi_df.iterrows():
    taxi_lat.append(row["latitude"])
    taxi_lon.append(row["longitude"])

plt.scatter(taxi_lon,taxi_lat,color="green")

plt.xlabel("longitude")
plt.ylabel("latitude")