from flask import Flask
import threading
import time
from flask import request
import json
import requests
import math
import AntColonyAlgo.ACO as aco
import matplotlib.pyplot as plt

app = Flask(__name__)
taxi_ip = ["5000","5001","5002"]
other_taxi_ip = ["5001","5002"]
url_taxi = "http://0.0.0.0:"

taxi = {'id': 1, 'currentLoc': [41.877406123,-87.621971652], 'noPassengers':0, 'passenger':[], 'direction':[]}
route = []
cost = 0
pheromone = aco.pheromone
evaporation_factor = 0.5
centroids = aco.centroids

def plot_route():

	lat = [taxi['currentLoc'][0]]
	lon = [taxi['currentLoc'][1]]
	ct = 0
	fig, ax = plt.subplots()
	ax.scatter(taxi['currentLoc'][1],taxi['currentLoc'][0])
	ax.annotate("cur",(taxi['currentLoc'][1],taxi['currentLoc'][0]))
	for i in taxi["direction"]:
		if "src" in i:
			ax.scatter(i["loc"][1],i["loc"][0])
			ax.annotate(str(ct+1)+"-"+i["name"]+"(s)",(i["loc"][1],i["loc"][0]))
			ct += 1
		if "dest" in i:
			ax.scatter(i["loc"][1],i["loc"][0])	
			ax.annotate(str(ct+1)+"-"+i["name"]+"(d)",(i["loc"][1],i["loc"][0]))
			ct += 1
		lat.append(i["loc"][0])
		lon.append(i["loc"][1])
	
	ax.plot(lon,lat,color='blue')

	fig.savefig("taxi"+str(taxi["id"]))
	plt.close()

def find_destination_reachingtime(name):
	reach_time = 0 
	start = 0

	for i in taxi["direction"]:
		reach_time += i["time"]
		if "name" in i:
			if i["name"]==name:
				if "dest" in i and i["dest"] == 1:
					break
	return reach_time

def find_pwaiting_time(name):
	pickup_time = 0
	for path in taxi["direction"]:
		pickup_time += path["time"]
		if "name" in path and path["name"] == name and "src" in path:
			break
	return pickup_time

def giveRegionsPassed(startPoint,endPoint): 
    URL = "https://route.api.here.com/routing/7.2/calculateroute.json?"

    way0 = "geo!" + str(startPoint[0]) + "," + str(startPoint[1])
    way1 = "geo!" + str(endPoint[0]) + "," + str(endPoint[1])


    PARAMS = {'app_id':'DbqcQH7pnhWqKqAFwiJB','app_code':'LfjixfoILHD4zRP4zktXHg', 'waypoint0':way0, 'waypoint1':way1 ,'mode':'fastest;car;traffic:disabled'} 
    
    r = requests.get(url = URL, params = PARAMS) 
    
    data = r.json() 

    allPositions = []
    allPositions.append({'loc':[data["response"]["route"][0]['leg'][0]['start']['originalPosition']['latitude'],data["response"]["route"][0]['leg'][0]['start']['originalPosition']['longitude']]   ,'time': 0})


    for i in data["response"]["route"][0]['leg'][0]['maneuver']:
        allPositions.append({'loc': [i['position']['latitude'],i['position']['longitude']], 'time': i['travelTime']})

    allPositions.append({'loc' :[data["response"]["route"][0]['leg'][0]['end']['originalPosition']['latitude'],data["response"]["route"][0]['leg'][0]['end']['originalPosition']['longitude']], 'time': i['travelTime']})

    return(allPositions)


def find_passenger_index(name):
    for i in range(0,len(taxi["passenger"])):
        if(taxi["passenger"][i]["name"]==name):
            return i
    raise Exception("passenger not found")

def update_passengerNo(index):
	no = taxi["passenger"][index]["passengerNo"] 
	if(no == 1):
		for i in taxi["passenger"]:
			if(i["passengerNo"]==2):
				i["passengerNo"]=1
			elif(i["passengerNo"]==3):
				i["passengerNo"]=2
			elif(i["passengerNo"]==4):
				i["passengerNo"]=3
	if(no==2):
		for i in taxi["passenger"]:
			if(i["passengerNo"]==3):
				i["passengerNo"]=2
			elif(i["passengerNo"]==4):
				i["passengerNo"]=3
	if(no==3):
		for i in taxi["passenger"]:
			if(i["passengerNo"]==4):
				i["passengerNo"]=3


def updateTaxi():
    print("Updated Taxi Data ")
    global taxi
    global t1

    for i in taxi["passenger"]:
        i["elapsedTime"] += taxi["direction"][0]["time"] #elapsed time is from the point the request was confirmed

    if(len(taxi["direction"])>=1):
        taxi["currentLoc"] = taxi['direction'][0]['loc']
        if("src" in taxi["direction"][0]):
            index = find_passenger_index(taxi["direction"][0]["name"])
            taxi["passenger"][index]["picked"] = 1
            print("passenger picked is :", taxi["passenger"][index]["name"])
        if("dest" in taxi["direction"][0]):
            index = find_passenger_index(taxi["direction"][0]["name"])
            taxi["noPassengers"] -= 1
            print("Your Fare is: ", taxi["passenger"][index]['fare'])
            #update passenegerNo in taxi[passeneger]:
            update_passengerNo(index)
            taxi["passenger"].pop(index)
            print("passenger dropped is:",taxi["direction"][0]["name"])
            print("current passengers are:",taxi["passenger"])
        taxi["direction"].pop(0)
        if(t1.is_alive):
            t1.cancel()
            start_route_timer()
    else:
        if(t1.is_alive):
            t1.cancel()
			

def start_route_timer():
	global t1
	print(taxi["direction"])
	if(len(taxi["direction"])!=0):
		t1 = threading.Timer(taxi["direction"][0]["time"],updateTaxi)
		t1.start()


def reset_route_timer():
	global t1
	if(t1.is_alive):
		t1.cancel()
		start_route_timer()


def check_src(pt,names,pass_array):
	for i in pass_array:
		if(str(i["src"])==str(pt) and i["name"] not in names):
			return True,i["name"]
	return False,None

def check_dest(pt,names,pass_array):
	for i in pass_array:
		if(str(i["dest"])==str(pt) and i["name"] not in names):
			return True,i["name"]
	return False,None

def check_dsttime_constraint():
	for i in taxi["passenger"]:
		rem_time = 0
		for j in direction:
			rem_time += j["time"]
			if "name" in j and j["name"]==i["name"]:
				if "dest" in j:
					break
		print("time for other passenger ", i["name"]," to reach is ",rem_time + i["elapsedTime"])
		if(rem_time + i["elapsedTime"] > i["DestReachTime"] + 600): 
			return False
	return True

def check_pwtime_constraint():
	for passenger in taxi["passenger"]:
		remaining_time = 0
		for path in direction:
			remaining_time += path["time"]
			if "name" in path and path["name"] == passenger["name"] and "src" in path:
				break
		print("Passenger ",passenger["name"]," needs to wait ",remaining_time + passenger["elapsedTime"],"sec")
		if  (remaining_time + passenger["elapsedTime"]) > (passenger["waitingTime"] + 300) :
			#if new passenger waiting time is more than 5 mins of previous passenger waiting time 
			return False
	return True

#This to avoid infinite loop of broadcast to all peers
broadcastDone = 0

def broadcastToAllPeers(data):
    costData = []
    costs = []
    for i in other_taxi_ip:
        r = requests.get(url=url_taxi+i+"/ping", params = {'src_lat': taxi['currentLoc'][0], 'src_lon': taxi['currentLoc'][1]})
        r = r.json()
        s = requests.get(url=url_taxi+i+"/ping", params = {'src_lat': data['src'][0], 'src_lon': data['src'][1]})
        s = s.json()
        if(int(s['distance']< 3000)):
            #"name" was passed in requests from passengers
            paramts = {'src_lat': data['src'][0], 'src_lon': data['src'][1], 'dest_lat': data['dest'][0], 'dest_lon': data['dest'][1], "name": data["name"]}
            r = requests.get(url=url_taxi+i+"/getRequest", params = paramts)
            r = r.json()  
            costData.append(r)
            costs.append(r['cost'])
    if(len(costs)==0):
        return({'cost':-1,'id' : taxi['id'], 'port':5000})
    return(costData[costs.index(min(costs))])

def get_distance_cost(startPoint,endPoint):
    if(str(startPoint)==str(endPoint)):
       return(0)
    URL = "https://route.api.here.com/routing/7.2/calculateroute.json?"

    way0 = "geo!" + str(startPoint[0]) + "," + str(startPoint[1])
    way1 = "geo!" + str(endPoint[0]) + "," + str(endPoint[1])


    PARAMS = {'app_id':'DbqcQH7pnhWqKqAFwiJB','app_code':'LfjixfoILHD4zRP4zktXHg', 'waypoint0':way0, 'waypoint1':way1 ,'mode':'fastest;car;traffic:disabled'} 
    
    r = requests.get(url = URL, params = PARAMS) 
    
    data = r.json() 

    distance = float(data["response"]["route"][0]["summary"]["distance"])
    return(distance/1000 * 4)
	
@app.route("/ping", methods = ['GET', 'POST'])
def pingRequest():
    recieved = request.args
    passLoc = [float(recieved['src_lat']),float(recieved['src_lon'])]
    x1,y1 = aco.convert_to_xy(passLoc)
    x2,y2 = aco.convert_to_xy(taxi['currentLoc'])   
    dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    return(json.dumps({'port': 5000, 'distance': dist}))
    
@app.route("/liveTrack", methods = ['GET', 'POST'])
def sendLocation():
    return(json.dumps({'curr' : taxi['currentLoc']}))

@app.route("/getRequest", methods = ['GET', 'POST'])
def processRequest():

    global taxi
    recieved = request.args

    acoVal = {'currentLoc': taxi['currentLoc'],'newReq':{'src': [float(recieved['src_lat']),float(recieved['src_lon'])],'dest': [float(recieved['dest_lat']),float(recieved['dest_lon'])], "name": recieved["name"]},'passengers': taxi['passenger']}

    global broadcastDone

    if(taxi['noPassengers'] >= 4):
        if broadcastDone == 1:
        	broadcastDone = 0
        	return (json.dumps({'id':taxi['id'], 'port': 5000, 'cost':-1}))
        broadcastDone = 1
        print("Passing to my neighbor because I have 4 passengers")
        return(json.dumps(broadcastToAllPeers(acoVal['newReq'])))

    dataRecv = aco.acoData(acoVal)

    global cost 

    cost = dataRecv['cost']

    #return value to passenger
    retVal = {'id': taxi['id'], 'port':5000, 'cost': cost}


    if(cost != -1):
       global route 
       route = [taxi["currentLoc"]]+dataRecv['route']

    else:
        if broadcastDone == 1:
             broadcastDone = 0
             return(json.dumps(retVal))
        broadcastDone = 1
        print("Passing to my neighbor because of Passenger waiting Time is more")
        return(json.dumps(broadcastToAllPeers(acoVal['newReq'])))

    #here if cost is -1 then directly broadcast to other peers??
    
    print("cost for taxi:",cost," and taxis current loc:",taxi["currentLoc"]) 

    global direction

    startPoint = route[0]
    direction = []
    names_src = []
    names_dst = []

    pass_array = taxi["passenger"]+[{'src': [float(recieved['src_lat']),float(recieved['src_lon'])],'dest': [float(recieved['dest_lat']),float(recieved['dest_lon'])],"name":recieved["name"]}]
    for i in route[1:]:
        path = giveRegionsPassed(startPoint,i)[:-1]
        res, name = check_src(i,names_src,pass_array)
        if(res):
           path[len(path)-1]['src'] = 1
           path[len(path)-1]['name'] = name
           names_src.append(name)
        res, name = check_dest(i,names_dst,pass_array)
        if(res):
           path[len(path)-1]['dest'] = 1
           path[len(path)-1]['name'] = name
           names_dst.append(name)
        direction += path
        startPoint = i

    #return value to passenger
    retVal = {'id': taxi['id'], 'port':5000, 'cost': cost}

    #check if passenger waiting time of all other current passengers changes a lot then broadcast request to other peers
    if(check_pwtime_constraint() == False):
        if broadcastDone == 1:
        	broadcastDone = 0
        	return(json.dumps(retVal))
        broadcastDone = 1
        print("Passing to my neighbor because of Passenger Waiting Time of other customer(s)")
        return(json.dumps(broadcastToAllPeers(acoVal['newReq'])))

    if(check_dsttime_constraint()==False):
        if broadcastDone == 1:
        	broadcastDone = 0
        	return(json.dumps(retVal))
        broadcastDone = 1
        print("Passing to my neighbor because of Passenger Destination Time of other customer(s)")
        return(json.dumps(broadcastToAllPeers(acoVal['newReq'])))

    
    #print("Prev cost and now cost",prevcost,cost,abs(prevcost - cost))
    return(json.dumps(retVal))

@app.route("/requestConfirm", methods = ['GET', 'POST'])
def confirmRequest():
    global taxi
    global direction

    recieved = request.args

    recieved = {'src': [float(recieved['src_lat']),float(recieved['src_lon'])],'dest': [float(recieved['dest_lat']),float(recieved['dest_lon'])],'name':recieved["name"]}

    fare = 78 + get_distance_cost(recieved['src'],recieved['dest'])

    taxi['noPassengers'] += 1

    taxi['passenger'].append({'src': recieved['src'], 'dest': recieved['dest'],'name':recieved["name"],"picked":0, 'fare': fare,'passengerNo':taxi['noPassengers'],"elapsedTime":0})

    taxi["direction"] = direction
    
    #the way destination reaching time is computed is from the time the passenger is picked up -- needs change
    reach_time = find_destination_reachingtime(recieved["name"])
    taxi["passenger"][len(taxi["passenger"])-1]["DestReachTime"] = reach_time 

    ''' Remember this passenger waiting time is from current location at the time request arrived (startpoint = route[0]) to new passenger's source from API
	Should we consider current location - what if it changed by the time ACO and request confirmation happended??'''

    #add passenger waiting time
    taxi["passenger"][taxi["noPassengers"]-1]["waitingTime"] = find_pwaiting_time(recieved["name"])
    
    if(taxi["noPassengers"]==1):
        start_route_timer()
    else:
        reset_route_timer()

    routeString = ""
    for i in route:
        routeString += str(i[0]) + "," + str(i[1]) + ";"
    routeString = routeString[:-1] 
    cost_params = {"route":routeString,"cost":cost}
    for i in taxi_ip:
        r = requests.get(url=url_taxi+i+"/broadcastPheromone",params=cost_params)

    plot_route()
    return json.dumps({'reach_time':reach_time,'fare':fare})

@app.route('/broadcastPheromone')
def pheromone_update():
    global pheromone
    received = request.args
    centroids_new = []
    route = received["route"]
    route = [list(map(float,i.split(','))) for i in route.split(";")]

    for i in route:
        pos = aco.convert_to_xy(i)
        pt = aco.get_nearest_centroid(pos)
        centroids_new.append(pt)
    for i in range(1,len(centroids_new)):
            pheromone[centroids_new[i-1]][centroids_new[i]] = (1-evaporation_factor)*pheromone[centroids_new[i-1]][centroids_new[i]] + evaporation_factor / float(received["cost"])
    print("pheromone matrix updated for taxi id:",taxi["id"])
    return("Broadcasting Done.")




if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000, debug = True)

