'''
Created By : Akshaykanth D L

This program gets all the regions that vehicle passes throught inorder to change the pheromene matrix
'''


import requests
import pandas as pd
import numpy as np 


###########################################################################

def getRegionIndex(allPositions, allmids):
    RegionsPassed = []
    for i in allPositions:
        curdist = []
        for j in allmids:
            curdist.append((i[0]-j[0])**2 + (i[1]-j[1])**2)
        RegionsPassed.append(curdist.index(min(curdist)))

    print(RegionsPassed)
    return(RegionsPassed)

######################################################################

def convert_to_xy(pos):
    lat,long_ = pos
    x = radius_earth *math.cos(math.radians(lat))*math.cos(math.radians(long_))
    y = radius_earth *math.cos((math.radians(lat)))*math.sin(math.radians(long_))
    return ([x,y])
##################################################################################

def giveRegionsPassed(startPoint,endPoint):
    # api-endpoint 
    URL = "https://route.api.here.com/routing/7.2/calculateroute.json?"

    #app_id=DbqcQH7pnhWqKqAFwiJB&app_code=LfjixfoILHD4zRP4zktXHg&waypoint0=geo!52.5,13.4&waypoint1=geo!52.5,13.45&mode=fastest;car;traffic:disabled"  
    
    # defining a params dict for the parameters to be sent to the API
    way0 = "geo!" + str(startPoint[0]) + "," + str(startPoint[1])
    way1 = "geo!" + str(endPoint[0]) + "," + str(endPoint[1])


    PARAMS = {'app_id':'DbqcQH7pnhWqKqAFwiJB','app_code':'LfjixfoILHD4zRP4zktXHg', 'waypoint0':way0, 'waypoint1':way1 ,'mode':'fastest;car;traffic:disabled'} 
    
    # sending get request and saving the response as response object 
    r = requests.get(url = URL, params = PARAMS) 
    
    # extracting data in json format 
    data = r.json() 


    '''
    print(data["response"]["route"][0]['leg'][0]['start'])
    print('########################################')
    print(data["response"]["route"][0]['leg'][0]['end'])
    print('########################################')
    print(data["response"]["route"][0]['leg'][0]['length'])
    print('########################################')
    print(len(data["response"]["route"][0]['leg'][0]['maneuver']))
    print('########################################')
    print(data["response"]["route"][0]['leg'][0]['travelTime'])
    '''
    for i in data["response"]["route"][0]['leg'][0]['maneuver']:
        print(i["length"])

    """

    #Adding the start Point to region Passed
    allPositions = []
    allPositions.append(convert_to_xy([data["response"]["route"][0]['leg'][0]['start']['originalPosition']['latitude'],data["response"]["route"][0]['leg'][0]['start']['originalPosition']['longitude']]))


    #Adding all the major regions the Vehicle passed
    for i in data["response"]["route"][0]['leg'][0]['maneuver']:
        allPositions.append(convert_to_xy([i['position']['latitude'],i['position']['longitude']]))

    #Adding the End Point to region Passed
    allPositions.append(convert_to_xy([data["response"]["route"][0]['leg'][0]['end']['originalPosition']['latitude'],data["response"]["route"][0]['leg'][0]['end']['originalPosition']['longitude']]))

    print(allPositions)
    return(allPositions)
    #return(getRegionIndex(allPositions,allmids))
    """

#################################################################################
print(giveRegionsPassed([41.878413, -87.6174152], [41.8984491, -87.6207688]))

'''
print("Loading Data...")
df = pd.read_csv("data_1000.csv", parse_dates=True)
centroids = list(np.load('centroids.npy'))

#print(centroids)

startLat = df['pickup_lat']
startLong = df['pickup_lon'] 
endLat = df['drop_lat']
endLong = df['drop_lon']

print("Finding Regions")
for i in range(len(startLat)):
    print(giveRegionsPassed([startLat[i], startLong[i]], [endLat[i], endLong[i]],centroids))
    break
'''
