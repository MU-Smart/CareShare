# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 19:54:47 2018

@author: Aishwarya
"""

import pandas as pd
import operator
import json

with open("./Extra_Chicago2016/column_remapping.json") as f:
    mapping = json.load(f)

df = pd.read_csv("./chicago_taxi_trips_2016_12_clean.csv")

df = df[pd.notnull(df['company'])]

taxi_company = {}

for i,row in df.iterrows():
    comp = row["company"]
    #comp = mapping["company"][str(int(row["company"]))]
    if row["company"] in taxi_company:
        taxi_company[comp] += 1
    else:
        taxi_company[comp] = 1
        
sorted_taxi_company = sorted(taxi_company.items(), key=operator.itemgetter(1))
'''
named_taxi_company = []
for i in sorted(taxi_company.items(), key=operator.itemgetter(1)):
    named_taxi_company.append([mapping["company"][str(int(i[0]))],i[1]])

'''
#consider taxis with highest servicing
sorted_taxi_company.reverse()
df_list = []
for i,row in df.iterrows():
    if(int(row["company"]) == int(sorted_taxi_company[0][0])):
        df_list.append(row)
     
new_df = pd.DataFrame(daywise_df_list)
new_df.to_csv("./chicago_taxi_trips_2016_12_clean_companywise.csv")
