import sys
import requests
import numpy
from rideShare_parameters import get_parameters

taxi = {'currentLoc': [41.900221297,-87.629105186]}

params = get_parameters()
radius_earth = 6371000


def convert_to_xy(pos):
	lat,long_ = pos
	x = radius_earth *math.cos(math.radians(lat))*math.cos(math.radians(long_))
	y = radius_earth *math.cos((math.radians(lat)))*math.sin(math.radians(long_))
	return (x,y)


def findPriority(features):
	startPoint = features[1]
	endPoint = features[0]
	URL = params["api_url"]

	way0 = "geo!" + str(startPoint[0]) + "," + str(startPoint[1])
	way1 = "geo!" + str(endPoint[0]) + "," + str(endPoint[1])

	PARAMS = {'app_id': params["app_id"],'app_code':params['app_code'], 'waypoint0':way0, 'waypoint1':way1 ,'mode':'fastest;car'} 
	r = requests.get(url = URL, params = PARAMS) 
	data = r.json()
	#print(data)
	distance = float(data["response"]["route"][0]["summary"]["distance"])
	return(distance)

def acquireRequest(recieved, requestQueue):
	#global requestQueue
	src = [float(recieved['src_lat']),float(recieved['src_lon'])]
	dest = [float(recieved['dest_lat']),float(recieved['dest_lon'])]
	#srcXY = convert_to_xy(src)
	taxiLoc = taxi['currentLoc']
	#taxiLocXY = convert_to_xy(taxiLoc)
	prior = findPriority([src, taxiLoc])

	if(len(requestQueue) == 0):
		requestQueue = [(recieved, prior)]
	else:
		for i  in range(len(requestQueue)):
			if( requestQueue[i][1] > prior):
				requestQueue.insert(i, (recieved, prior))
				break
						
		if(requestQueue[-1][1] < prior):
			requestQueue.append((recieved, prior))
	return(requestQueue)



def feed(requestQueue):
	return(requestQueue.pop(0)[0])


def deleteRequest(reqName, requestQueue):
	
	for i in range(len(requestQueue)):
		if(requestQueue[i][0]["name"]  == reqName):
			del requestQueue[i]
			print("Deleted Request: " , reqName)
			break
	
	return(requestQueue)				


def findRequest(reqName, requestProcessed):

	for i in range(len(requestProcessed)):
		if(requestProcessed[i]["name"]  == reqName):
			return(i)
			
	return(-1)				
	

