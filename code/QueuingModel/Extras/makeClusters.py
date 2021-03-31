"""
Clustering of pickup locations based on request origin
"""

#############################################################################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from equal_groups import EqualGroupsKMeans


#############################################################################

print("Loading Data...")
df = pd.read_csv("chicago_taxi_trips_2016_12.csv", parse_dates=True)
#print(df['pickup_latitude'][:100])

pickUpLat = np.array(df['pickup_latitude'])
pickUpLong = np.array(df['pickup_longitude'])
pickUpLat = pickUpLat[~np.isnan(pickUpLat)]
pickUpLong = pickUpLong[~np.isnan(pickUpLong)]
cordinates = np.vstack((pickUpLat, pickUpLong)).T
print("Total Data : ", len(cordinates))

print("Clustering...")
kmeans_main = KMeans(n_clusters=8).fit(cordinates[:500])
kmeans = EqualGroupsKMeans(n_clusters=8).fit(cordinates[:500])
centers_main = kmeans_main.cluster_centers_
centers = kmeans.cluster_centers_
x = [i[0] for i in centers]
y = [i[1] for i in centers]
x_m = [i[0] for i in centers_main]
y_m = [i[1] for i in centers_main]

plt.scatter(pickUpLat, pickUpLong, alpha=0.5)
plt.scatter(x_m,y_m,c='green', s=200)
plt.scatter(x,y,c='red', s=200)
plt.title('Scatter plot of pickups')
plt.xlabel('Latitude')
plt.ylabel('Longitutde')
plt.show()