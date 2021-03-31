import numpy as np
import random
import math 
import requests
from rideShare_parameters import get_parameters

#key='AIzaSyBHuwu35zy5pOoDxOxpy4ErdqqtkvBCJK4'

params = get_parameters()


radius_earth = 6371000
lambda_parameter = float(params["lambda_parameter"])

'''
def reverse_geocoder(loc):
	return gmaps.reverse_geocode(loc)['address_components']['formatted_address']


def get_distance_time(locA, locB):
	src = str(locA[0])+","+str(locA[1])
	dest = str(locB[0])+","+str(locB[1])
	url ='https://maps.googleapis.com/maps/api/distancematrix/json?'
	r = requests.get(url + 'origins=' + src +
                   '&destinations=' + dest +
                   '&key=' + key)
                     
	# json method of response object 
	# return json format result 
	response = r.json()
	return response['rows'][0]['elements'][0]['distance']['value']

def get_centroid_index(pos):
	lat,long_ = pos
	for (i,cnt) in enumerate(centroids):
		if lat == cnt[0] and long_ == cnt[1]:
			return i
	return None
'''
def get_distance_time(startPoint,endPoint):
    if(str(startPoint)==str(endPoint)):
       return [0.001,0.001]
    URL = params["api_url"]

    way0 = "geo!" + str(startPoint[0]) + "," + str(startPoint[1])
    way1 = "geo!" + str(endPoint[0]) + "," + str(endPoint[1])


    PARAMS = {'app_id': params["app_id"],'app_code':params['app_code'], 'waypoint0':way0, 'waypoint1':way1 ,'mode':'fastest;car'} 
    
    r = requests.get(url = URL, params = PARAMS) 
    
    data = r.json() 

    distance = float(data["response"]["route"][0]["summary"]["distance"])
    if(int(distance)==0):
        distance = 0.001

    traffic_time = float(data["response"]["route"][0]["summary"]["trafficTime"])
    if(int(traffic_time)==0):
        trafficTime = 0.001
    return [distance,traffic_time]


def convert_to_xy(pos):
	lat,long_ = pos
	x = radius_earth *math.cos(math.radians(lat))*math.cos(math.radians(long_))
	y = radius_earth *math.cos((math.radians(lat)))*math.sin(math.radians(long_))
	return (x,y)

def get_nearest_centroid(pos):
	x,y = pos
	dist = []
	for (i,cnt) in enumerate(centroids):
		dist.append(((x-cnt[0])**2 + (y-cnt[1])**2)**(1/2))
	return dist.index(min(dist))
		
def find_prob(src, dest,centroids_latlng):
	result = get_distance_time(src['latlng'], dest['latlng'])
	distance = result[0]
	traffic_time = result[1]
	locA = src['cnt']
	locB = dest['cnt']
	try:
		return pheromone[locA,locB]*((1/distance)**(beta*lambda_parameter))*((1/traffic_time)**(beta*(1-lambda_parameter)))
	except ZeroDivisionError:
		return pheromone[locA,locB]*((1.0/0.001)**(beta*lambda_parameter))*((1.0/0.001)**(beta*(1-lambda_parameter)))

#pre-computed centroids from grids
centroids = np.load(params["centroids_file"])
n_cities = centroids.shape[0]

#weightage for visibility
beta = float(params["beta"])

#initialize pheromone
pheromone = np.random.rand(n_cities,n_cities)


def ifPickup(loc, pickups):
	'''
	This function checks if loc is in pickups and returns the index if found else
	returns None
	'''
	for (i,src) in enumerate(pickups):
		if loc[0] == src[0] and loc[1] == src[1]:
			return i
	return None

def acoData(params):
	#list of passengers already in the taxi
	serving_requests = params['passengers']

	pickups = []
	dropoffs = []
	
	nodes_to_visit = []
	for node in serving_requests:
		if node['picked'] == 0:
			pickups.append(node['src'])
			dropoffs.append(node['dest'])
		else:
			nodes_to_visit.append(node['dest'])

	if(len(pickups) > 0):
		print("src exists:",pickups)

	curr_loc = get_nearest_centroid(convert_to_xy(params['currentLoc']))

	new_request = params['newReq']
	print("New Request:", new_request)

	#ACO loop
	route_centroids = []
	route_latlng = []

	pickups.append(new_request['src'])
	dropoffs.append(new_request['dest'])


	nodes_to_iterate = nodes_to_visit + pickups

	n = len(nodes_to_iterate) + len(dropoffs)
	print("nodes to iterate:", nodes_to_iterate)
	centroids_nodes = list(map(get_nearest_centroid,map(convert_to_xy,nodes_to_iterate)))

	locA = {'cnt':curr_loc, 'latlng' : params['currentLoc'] }
	#route_centroids.append(locA['cnt'])
	#route_latlng.append(locA['latlng'])
	for i in range(n):
		max_prob = 0	
		locB = None
		for (ind,node) in enumerate(nodes_to_iterate):
			
			prob = find_prob(locA,{'latlng':node, 'cnt':centroids_nodes[ind]},nodes_to_iterate)
			if prob > max_prob:
				locB = {'latlng':node, 'cnt':centroids_nodes[ind]}
				max_prob = prob
		if locB is not None:
			pickup_idx = ifPickup(locB['latlng'],pickups)
			if pickup_idx is not None:
				nodes_to_iterate.append(dropoffs[pickup_idx])
				pickups.remove(locB['latlng'])
				centroids_nodes.append(get_nearest_centroid(convert_to_xy(dropoffs[pickup_idx])))
				dropoffs.pop(pickup_idx)
			route_centroids.append(locB['cnt'])
			route_latlng.append(locB['latlng'])
		else:
			raise Exception("Error Finding Route: Next Block")
	
		locA = locB
		nodes_to_iterate.remove(locB['latlng'])
		centroids_nodes.remove(locB['cnt'])



	time_to_src = 0
	locA = params['currentLoc']

	for (i,node) in enumerate(route_latlng):	
		if node[0] == new_request["src"][0] and node[1] == new_request["src"][1]:
			time_to_src += get_distance_time(locA,route_latlng[i])[1]
			break
	
		time_to_src += get_distance_time(locA,route_latlng[i])[1]
		locA = route_latlng[i]

	passenger_waiting_time = time_to_src
	print("Passenger Waiting Time: ",passenger_waiting_time)
	if passenger_waiting_time > 600:
		return {'route':[],'cost': -1,'pwt':passenger_waiting_time}

	#Optimize this while using google API store distances that to request from the API
	locA = params['currentLoc']
	cost_dist = 0
	cost_time = 0

	#cost is modelled only with respect to taxi's whole travel distance -- need to consider other parameters
	for node in route_latlng:
		cost_dist += get_distance_time(locA,node)[0]
		cost_time += get_distance_time(locA,node)[1]
		locA = node
	
	print("\n\nRoute:",route_latlng,"\n\n")
	return {'route':route_latlng, 'cost': cost_dist ,'cost_time':cost_time}

