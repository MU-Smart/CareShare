# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 18:55:15 2018

@author: Aishwarya
"""

import pandas as pd

#read the dataframe
df = pd.read_csv("./chicago_taxi_trips_2016_12.csv")

#remove rows where values of dropoff and pickup locations, fare of the trip and time of trip  are null
df = df.dropna(axis=0, subset=['pickup_latitude','dropoff_latitude','trip_seconds','fare'])

#nan_rows = df[df['pickup_latitude'].isnull()]#this chceks if a certain column has nan

#remove trips with trip time less than 5 minutes 
df = df[df.trip_seconds > 300]

#remove trips with fare = 0
df = df[df.fare > 0]

''''
#to recheck
for i,row in df.iterrows():
    if(row["fare"]<=0):
        print(row)
    if(row["trip_seconds"]<=300):
        print(row)
'''
        
#for a particular day
daywise_df_list = []
for i,row in df.iterrows():
    if(row["trip_start_timestamp"].split(' ')[0]=='2016-12-1'):
        daywise_df_list.append(row)
        
daywise_df = pd.DataFrame(daywise_df_list)

daywise_df.to_csv("./chicago_taxi_trips_2016_12_clean.csv")