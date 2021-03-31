# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 09:17:30 2018

@author: Aishwarya
"""
import pprint
import googlemaps
from datetime import datetime


api_key = "AIzaSyAvXh0nxTBFn5qJIXTr7K9h0IvJ8P8Nmug"


gmaps = googlemaps.Client(key=api_key)
print(gmaps)

now = datetime.now()
directions_result = gmaps.directions("The Embarcadero, San Francisco","Alcatraz Island, San Francisco",mode="transit",departure_time=now)

#print(directions_result)



pprint.pprint(directions_result[0]['legs'][0])
'''for i in directions_result[0]:
    print(i)
    print("************************")
    https://route.api.here.com/routing/7.2/calculateroute.json?app_id={DbqcQH7pnhWqKqAFwiJB}&app_code={LfjixfoILHD4zRP4zktXHg}&waypoint0=geo!52.5,13.4&waypoint1=geo!52.5,13.45&mode=fastest;car;traffic:disabled
    
    
    '''