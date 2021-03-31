# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 20:33:17 2018

@author: Aishwarya
"""

import pandas as pd
import random
import datetime
import matplotlib.pyplot as plt

def random_date(start, end):
    """Generate a random datetime between `start` and `end`"""
    return start + datetime.timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

df = pd.read_csv("./chicago_taxi_trips_2016_12_clean.csv")

new_df = []
for i,row in df.iterrows():
    dt_obj_start = datetime.datetime.strptime(row["trip_start_timestamp"].split(' ')[1],"%H:%M:%S")
    rand_starttime = random_date(dt_obj_start,dt_obj_start + datetime.timedelta(minutes=15)).strftime("%H:%M:%S")
    
    dt_obj_stop = datetime.datetime.strptime(row["trip_end_timestamp"].split(' ')[1],"%H:%M:%S")
    rand_stopttime = random_date(dt_obj_stop,dt_obj_stop + datetime.timedelta(minutes=15)).strftime("%H:%M:%S")
    
    row["trip_start_timestamp"] = rand_starttime
    row["trip_end_timestamp"] = rand_stopttime
    
    new_df.append(row)
    
new_df = pd.DataFrame(new_df)
new_df.to_csv("./chicago_taxi_trips_2016_12_clean_randomtime.csv")


time_interval1 = {"00:00:00":0,"01:00:00":0,"02:00:00":0,"03:00:00":0,"04:00:00":0,"05:00:00":0,"06:00:00":0,
    "07:00:00":0,"08:00:00":0,"09:00:00":0,"10:00:00":0,"11:00:00":0}

time_interval2 = {"12:00:00":0,"13:00:00":0,"14:00:00":0,"15:00:00":0,"16:00:00":0,"17:00:00":0,"18:00:00":0,
        "19:00:00":0,"20:00:00":0,"21:00:00":0,"22:00:00":0,"23:00:00":0}


for i,row in new_df.iterrows():
    for k in time_interval1:
        range1 = datetime.datetime.strptime(k,"%H:%M:%S")
        range2 = range1 + datetime.timedelta(minutes=60)
        inp = datetime.datetime.strptime(row["trip_start_timestamp"],"%H:%M:%S")
        if(inp > range1 and inp < range2):
            time_interval1[k] += 1
            break
#print(time_interval1)

for i,row in new_df.iterrows():
    for k in time_interval2:
        range1 = datetime.datetime.strptime(k,"%H:%M:%S")
        range2 = range1 + datetime.timedelta(minutes=60)
        inp = datetime.datetime.strptime(row["trip_start_timestamp"],"%H:%M:%S")
        if(inp > range1 and inp < range2):
            time_interval2[k] += 1
            break
#print(time_interval2)

key = [i.split(":")[0] for i in list(time_interval1.keys())+list(time_interval2.keys())]
value = list(time_interval1.values())+list(time_interval2.values())

#print(key,value)
plt.bar(key, value, color="blue")
plt.xlabel("time")
plt.ylabel("no of requests")