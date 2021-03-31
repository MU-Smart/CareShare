# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 07:02:30 2018

@author: Aishwarya
"""
import matplotlib.pyplot as plt
import geojson
import math
import numpy as np

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
            x_coordinates.append(radius_earth *math.cos(math.radians(k[1]))*math.cos(math.radians(k[0])))
            y_coordinates.append(radius_earth *math.cos((math.radians(k[1])))*math.sin(math.radians(k[0])))
        break


print(len(x_coordinates),max(x_coordinates),min(x_coordinates))
print(len(y_coordinates),max(y_coordinates),min(y_coordinates))


plt.plot(x_coordinates,y_coordinates)

#x_coordinates.sort()

pt = min(x_coordinates)
pt_x = []

while(pt<=max(x_coordinates)):
    plt.axvline(x=pt,color='yellow')
    #print(pt)
    pt_x.append(pt)
    pt += 3000
    
#y_coordinates.sort()

pt = min(y_coordinates)
pt_y = []
while(pt<=max(y_coordinates)):
    plt.axhline(y=pt,color='yellow')
    pt_y.append(pt)
    pt += 3000
    
print(pt_x,pt_y)
plt.title("Map of Chicago with 3km sq grids")

centroids = []

for i in range(1,len(pt_x)):
    x = (pt_x[i] + pt_x[i-1])/2
    for j in range(1,len(pt_y)):
        centroids.append([x,(pt_y[j]+pt_y[j-1])/2])
        
centroids = np.array(centroids)
        
np.save(centroids)
plt.scatter(centroids[:,0],centroids[:,1])
