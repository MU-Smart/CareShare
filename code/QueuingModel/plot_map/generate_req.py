import numpy as np
from column_remap import remap
import pandas as pd
import os
import random

'''
df = pd.read_csv("../chicago_taxi_trips_2016_12.csv",nrows=500)
 
pickup = []
dropoff = []
for i,row in df.iterrows():
    try:
        if((row["pickup_latitude"]!='nan' and row["pickup_latitude"]!='NaN') and (row["dropoff_latitude"]!='nan' and row["dropoff_latitude"]!='NaN')):
            #print(remap(row["pickup_latitude"],"pickup_latitude"))
            pickup.append(np.array([remap(row["pickup_latitude"],"pickup_latitude"),remap(row["pickup_longitude"],"pickup_longitude")]))
            dropoff.append(np.array([remap(row["dropoff_latitude"],"dropoff_latitude"),remap(row["dropoff_longitude"],"dropoff_longitude")]))
    except ValueError:
        continue

np.save("Requests.npy",np.array([pickup,dropoff]))
print(np.shape(pickup))
print(np.shape(dropoff))
'''

pickup, dropoff = np.load('Requests.npy')

requests = []
for i in range(30):
	requests.append(np.array([pickup[i][0],pickup[i][1], dropoff[i][0], dropoff[i][1], 'a'+str(i+1), random.randint(3,20)]))

import csv

with open('pass_req1.csv','w') as file_:
	writer = csv.writer(file_)
	writer.writerows(requests)
