# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 15:04:51 2018

@author: Aishwarya
"""

import json
import pandas as pd
import numpy as np

def load_mapping():
    with open("./column_remapping.json") as f:
        mapping = json.load(f)
    return mapping
'''
df = pd.read_csv("chicago_taxi_trips_2016_01.csv")
df = df[pd.notnull(df['pickup_latitude'])]
df = df[pd.notnull(df['dropoff_latitude'])]

data_pickup = []
#data_dropoff = []

for i in df["pickup_latitude"]:
    data_pickup.append((float(mapping['pickup_latitude'][str(int(i))]),abs(float(mapping['pickup_longitude'][str(int(i))]))))
    #data_dropoff.append((float(mapping['dropoff_latitude'][str(int(i))]),abs(float(mapping['dropoff_longitude'][str(int(i))]))))

np.save("chicago_taxi_trips_2016_01_pickupLatLon.npy",data_pickup)
'''
def remap(data,column):
    mapping = load_mapping()
    #print(data)
    return float(mapping[column][str(int(data))])
#print(load_mapping())
