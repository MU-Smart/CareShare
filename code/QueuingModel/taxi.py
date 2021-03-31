from flask import Flask
import threading
import time
import datetime
import sys
from flask import request
import json
import requests
import math
import AntColonyAlgo.ACO as aco
import matplotlib
import random
matplotlib.use("agg")
import matplotlib.pyplot as plt
from rideShare_parameters import get_parameters
from queueModel import *

app = Flask(__name__)


requestQueue = []
requestProcessed = []
taxi_id = sys.argv[1]
cur_lat = float(sys.argv[2])
cur_lon = float(sys.argv[3])

params = get_parameters()

no_of_taxis = int(params["no_of_taxis"])
start_port = int(params["start_port"])

taxi_ip = [str(start_port+i) for i in range(no_of_taxis)]
other_taxi_ip = list(set(taxi_ip) - set([taxi_id]))
url_taxi = params["url_taxi_ip"]


taxi = {'id': int(taxi_id)-start_port+1, 'currentLoc': [cur_lat,cur_lon], 'noPassengers':0, 'passenger':[], 'direction':[], 'total_dist':0, 'total_time':0}

route = []
cost = 0
no_messages = 0
time_with_passenger = 0
dist_with_2ormore_passengers = 0
shortest_path_api = 0
shortest_path_aco = 0

#Store these values as returned by ACO - send to passenger after confirmation (pareto)
detour_cost = None
tot_time_cost = None

broadcast_firsthop_costData = []
broadcast_firsthop_costs = []

#variables that store the total distance and total travel time of the direction computed for
#new request - this stored value is set to taxi when the request is confirmed
direction_dist = 0
direction_time = 0


pheromone = aco.pheromone
evaporation_factor = float(params["evaporation_factor"])
centroids = aco.centroids
taxi_total_dist = 0
taxi_detour_dist = 0
request_in_process = {"status":False,"passenger_name":""}


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

	fig.savefig("routes/taxi"+str(taxi["id"]))
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

def get_distance_aco(name):
	dist_src_dst = 0
	start = 0
	for i in taxi["direction"]:
		if "name" in i and i["name"]== name and "src" in i:
			start = 1
		if start == 1 and "name" in i and i["name"]== name and "dest" in i:
			dist_src_dst += i["dist"]
			break
		if start == 1:
			dist_src_dst += i["dist"]
	return dist_src_dst

def giveRegionsPassed(startPoint,endPoint, return_dist = False, return_time = False): 
    URL = params["api_url"]

    way0 = "geo!" + str(startPoint[0]) + "," + str(startPoint[1])
    way1 = "geo!" + str(endPoint[0]) + "," + str(endPoint[1])


    PARAMS = {'app_id': params["app_id"],'app_code':params['app_code'], 'waypoint0':way0, 'waypoint1':way1 ,'mode':'fastest;car'} 
    
    r = requests.get(url = URL, params = PARAMS) 
    
    data = r.json()

    if(return_time == True):
         time = float(data["response"]["route"][0]["summary"]["trafficTime"])
         if(time == 0.0):
              return 0.001
         return time

    if(return_dist == True):
         distance = float(data["response"]["route"][0]["summary"]["distance"])
         if(int(distance)==0):
             distance = 0.001
         return distance

    allPositions = []
    allPositions.append({'loc':[data["response"]["route"][0]['leg'][0]['start']['originalPosition']['latitude'],data["response"]["route"][0]['leg'][0]['start']['originalPosition']['longitude']]   ,'time': 0,'dist':0})


    for i in data["response"]["route"][0]['leg'][0]['maneuver']:
        allPositions.append({'loc': [i['position']['latitude'],i['position']['longitude']], 'time': i['travelTime'],'dist':i["length"]})

    allPositions.append({'loc' :[data["response"]["route"][0]['leg'][0]['end']['originalPosition']['latitude'],data["response"]["route"][0]['leg'][0]['end']['originalPosition']['longitude']], 'time': i['travelTime'],'dist':i["length"]})

    return(allPositions)


def find_passenger_index(name):
    for i in range(0,len(taxi["passenger"])):
        if(taxi["passenger"][i]["name"]==name):
            return i
    raise Exception("passenger not found:",name," and taxi is : ",taxi["passenger"], " \n", taxi)

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
    global taxi_total_dist
    global time_with_passenger
    global dist_with_2ormore_passengers

    for i in taxi["passenger"]:
        i["elapsedTime"] += taxi["direction"][0]["time"] #elapsed time is from the point the request was confirmed

    if(len(taxi["direction"])>=1):
        taxi["currentLoc"] = taxi['direction'][0]['loc']

        taxi_total_dist += taxi["direction"][0]["dist"] #to calculate total distance travelled by tax
        if(taxi["noPassengers"]>=2):
            dist_with_2ormore_passengers += taxi["direction"][0]["dist"] #calc denominator of distance ratio of ride sharing
            time_with_passenger += taxi["direction"][0]["time"]#to calculate total time spent by taxi when there are 2 or more passenger

        if("src" in taxi["direction"][0]):
            #wait randomly for (0-2minutes before picking passenger)
            index = find_passenger_index(taxi["direction"][0]["name"])
            if(taxi["noPassengers"]>=1):
                 rand_pwt_sleep = random.randint(1,120)
                 print("waiting for ",rand_pwt_sleep," to pick up passenger:",taxi["passenger"][index]["name"])
                 time.sleep(rand_pwt_sleep)
            taxi["passenger"][index]["picked"] = 1
            print("passenger picked is :", taxi["passenger"][index]["name"])

        if("dest" in taxi["direction"][0]):
            index = find_passenger_index(taxi["direction"][0]["name"])
            taxi["noPassengers"] -= 1
            #print("Your Fare is: ", taxi["passenger"][index]['fare'])
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


def start_confirm_timer(name):
	global request_in_process_timer
	global request_in_process
	request_in_process["status"] = True
	request_in_process["passenger_name"] = name
	print("Waiting for confirmation of ...",name)
	request_in_process_timer = threading.Timer(int(params["confirm_timer"]),reset_confirm_timer)
	request_in_process_timer.start()


def reset_confirm_timer():
	global request_in_process
	print("resetting confirm timer of ...",request_in_process["passenger_name"])
	global request_in_process_timer
	if(request_in_process_timer.is_alive):
		request_in_process_timer.cancel()
	request_in_process["status"] = False
	request_in_process["passenger_name"] = ""


def check_src(pt,names,pass_array):
	for i in pass_array:
		if(str(i["src"])==str(pt) and i["name"] not in names and i["picked"]==0):
			return True,i["name"]
	return False,None

def check_dest(pt,names,names_src,pass_array):
	for i in pass_array:
		if(str(i["dest"])==str(pt) and i["name"] not in names):
			if(i["name"] in names_src or i["picked"]==1):
				return True,i["name"]
	return False,None

def check_dsttime_constraint():
	for i in taxi["passenger"]:
		rem_time = 0
		for j in taxi["direction"]:
			rem_time += j["time"]
			if "name" in j and j["name"]==i["name"]:
				if "dest" in j:
					print("time for other passenger ", i["name"]," to reach is ",rem_time + i["elapsedTime"])
					if(rem_time + i["elapsedTime"] > i["DestReachTime"] + int(params["delta_drt"])): 
						return False
					break
		
	return True

def check_pwtime_constraint():
	for passenger in taxi["passenger"]:
		remaining_time = 0
		for path in taxi["direction"]:
			remaining_time += path["time"]
			if "name" in path and path["name"] == passenger["name"] and "src" in path:
				print("Passenger ",passenger["name"]," needs to wait ",remaining_time + passenger["elapsedTime"],"sec")
				if  (remaining_time + passenger["elapsedTime"]) > (passenger["waitingTime"] + int(params['delta_pwt'])) :
					#if new passenger waiting time is more than 10 mins of previous passenger waiting time 
					return False
				break
	return True

def send_request_broadcast_pheromone(i,cost_params):
	try:
		r = requests.get(url=url_taxi+i+"/broadcastPheromone",params=cost_params,timeout=int(params['request_timers']))
	except Exception as e: print(e)

def send_request_first_hop(i,paramts):
    global broadcast_firsthop_costData
    global broadcast_firsthop_costs
    paramts["othertaxi"] = i

    try:
           r = requests.get(url=url_taxi+i+"/getRequest", params = paramts, timeout=int(params['request_timers']))
           r = r.json()  
           broadcast_firsthop_costData.append(r)
           broadcast_firsthop_costs.append(r['cost'])
    except Exception as e: print(e)


def broadcastToAllPeers(data):
    global broadcast_firsthop_costData
    global broadcast_firsthop_costs
    global no_messages

    broadcast_firsthop_costData = []
    broadcast_firsthop_costs = []

    if((datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M:%S"),"%H:%M:%S")-(datetime.datetime.strptime(data["timestamp"],"%H:%M:%S"))).total_seconds() > (int(params['request_timers']) - 5)):
        print("Not broadcasting because :",(datetime.datetime.now()-(datetime.datetime.strptime(data["timestamp"],"%H:%M:%S"))).total_seconds())
        return json.dumps({'id':taxi['id'], 'port': int(taxi_id), 'cost':-1,"message":"Not broadcasting to peers because of delay"})

    r = requests.get(url=url_taxi + params["seeder_port"] + "/getTaxisNearby", params = {'src_lat': taxi['currentLoc'][0], 'src_lon': taxi['currentLoc'][1],'first_hop':1})
    r = r.json()
    if r['taxis'] == '[]':
        other_taxi_ip = []
    else:
        taxi_ids = list(r['taxis'])
        all_broadcasted_taxis = list(data["all_broadcasted_taxis"])
        other_taxi_ip = list(set([str(start_port + (int(temp_taxi_id)-1)) for temp_taxi_id in taxi_ids]) -set(all_broadcasted_taxis)) 

    paramts = {'src_lat': data['src'][0], 'src_lon': data['src'][1], 'dest_lat': data['dest'][0], 'dest_lon': data['dest'][1], "name": data["name"],'first_hop':1,'mytaxi':taxi_id,"timestamp":data['timestamp'],"all_broadcasted_taxis":" ".join(str(x) for x in other_taxi_ip)}
    if(len(other_taxi_ip)>0):
       no_messages += 1#broadcast message
    threads_firsthop = [threading.Thread(target=send_request_first_hop, args=(i,paramts,)) for i in other_taxi_ip]
    for thread in threads_firsthop:
        thread.start()
    for thread in threads_firsthop:
        thread.join()

    no_messages += len(other_taxi_ip)#reply from taxi message

    if(len(broadcast_firsthop_costs)==0):
        return({'cost':-1,'id' : taxi['id'], 'port':int(taxi_id),"message":"No taxis in second hop to broadcast"})
    return(broadcast_firsthop_costData[broadcast_firsthop_costs.index(min(broadcast_firsthop_costs))])

def get_distance_api(startPoint,endPoint):
    if(str(startPoint)==str(endPoint)):
       return(0)
    URL = params["api_url"]

    way0 = "geo!" + str(startPoint[0]) + "," + str(startPoint[1])
    way1 = "geo!" + str(endPoint[0]) + "," + str(endPoint[1])


    PARAMS = {'app_id':params["app_id"], 'app_code':params["app_code"], 'waypoint0':way0, 'waypoint1':way1 ,'mode':'fastest;car'} 
    
    r = requests.get(url = URL, params = PARAMS) 
    
    data = r.json() 

    distance = float(data["response"]["route"][0]["summary"]["distance"])
    return(distance)
	
@app.route("/ping", methods = ['GET', 'POST'])
def pingRequest():
    recieved = request.args
    passLoc = [float(recieved['src_lat']),float(recieved['src_lon'])]
    x1,y1 = aco.convert_to_xy(passLoc)
    x2,y2 = aco.convert_to_xy(taxi['currentLoc'])   
    dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    return(json.dumps({'port': int(taxi_id), 'distance': dist}))
    
@app.route("/liveTrack", methods = ['GET', 'POST'])
def sendLocation():
    return(json.dumps({'curr' : taxi['currentLoc']}))

@app.route("/getRequest", methods = ['GET', 'POST'])
def requestAccomodation():
   global requestQueue
   global requestProcessed

   recieved = request.args
   requestQueue = acquireRequest(recieved, requestQueue)
   while(findRequest(recieved["name"], requestProcessed) == -1):
       continue
   return(json.dumps(requestProcessed.pop(findRequest(recieved["name"], requestProcessed))))



@app.before_first_request
def activateJob():
	def processRequest():

		global taxi
		global request_in_process
		global no_messages
		global requestQueue
		global requestProcessed

		while(True):
			while(len(requestQueue) == 0):
				#print("Request Queue Empty")
				continue
			print("Request Queue: ", requestQueue)	    	    
			recieved = feed(requestQueue)
			if((datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M:%S"),"%H:%M:%S")-(datetime.datetime.strptime(recieved["timestamp"],"%H:%M:%S"))).total_seconds() > int(params["request_timers"])):
				return json.dumps({'id':taxi['id'], 'port': int(taxi_id), 'cost':-1,"message":"7.queued reaching taxi late"})

			broadcast_taxis = recieved["all_broadcasted_taxis"].split(" ")

			acoVal = {'currentLoc': taxi['currentLoc'],'newReq':{'src': [float(recieved['src_lat']),float(recieved['src_lon'])],'dest': [float(recieved['dest_lat']),float(recieved['dest_lon'])], "name": recieved["name"],"all_broadcasted_taxis": broadcast_taxis, 'timestamp':recieved["timestamp"]},'passengers': taxi['passenger']}

			global cost

			'''
		    	check if taxi is waiting for someone other passenger's confirmation
			'''

			if(request_in_process["status"]==True):
				requestProcessed.append({'name': recieved["name"],'id':taxi['id'], 'port': int(taxi_id), 'cost':-1,'message':"1.waiting for others pass confirmation"})
				continue			

			if(taxi['noPassengers'] >= 4):
				if 'first_hop' in request.args:
					requestProcessed.append({'name': recieved["name"],'id':taxi['id'], 'port': int(taxi_id), 'cost':-1,"message":"2.capacity"})
			     
				else:
					print("Passing to my neighbor because I have 4 passengers")
					requestProcessed.append(broadcastToAllPeers(acoVal['newReq']))
				continue

			dataRecv = aco.acoData(acoVal)

		  	#here cost is only total travel distance
			recv_cost = dataRecv['cost']

		    #return value to passenger
			retVal = {'name': recieved["name"], 'id': taxi['id'], 'port':int(taxi_id), 'cost': recv_cost,'detour_obj':0,'time_obj':0}


			if(recv_cost != -1):

		       #use these values for setting taxi['total_dist'] and taxi['total_time'] after request confirms
			       global direction_dist
			       global direction_time

			       direction_dist = recv_cost
			       direction_time = dataRecv['cost_time']

			       #declare the global cost variables (pareto)
			       global detour_cost
			       global tot_time_cost


			       '''
			       #computing detour time for the new request - use this when 
			       #objective function for peak hours changes
			       if(taxi['noPassengers'] == 0):
				    detour_time = giveRegionsPassed(taxi['currentLoc'], dataRecv['route'][0], return_time = True)
			       else:
				    detour_time = abs(dataRecv['cost_time'] - taxi['total_time'])

			       if detour_time != 0.0:
				    cost = math.sqrt(detour_time**2+dataRecv['cost_time']**2)
			       else:
				    cost =  math.sqrt(0.001**2+dataRecv['cost_time']**2)

			       #save detour cost value (pareto)
			       detour_cost = detour_time

			       print("Detour time for taxi",int(taxi['id']),"= ",detour_time)
			       '''

			       #not sure if absolute is necessary
			       if(taxi['noPassengers'] == 0):
				        detour_distance = giveRegionsPassed(taxi['currentLoc'], dataRecv['route'][0], return_dist = True)
			       else:
				        detour_distance = abs(recv_cost - taxi['total_dist'])

			       if detour_distance !=  0.0:
				        cost = math.sqrt(detour_distance**2+dataRecv['cost_time']**2)
			       else:
				        cost =  math.sqrt(0.001**2+dataRecv['cost_time']**2)

			       #save detour cost value (pareto)
			       detour_cost = detour_distance

			       print("Detour distance for taxi",int(taxi['id']),"= ",detour_distance," and time = ",dataRecv['cost_time'])
			       retVal["detour_obj"] =  detour_distance
			       retVal["time_obj"] = dataRecv['cost_time']

			       #save total travel cost value (pareto)
			       tot_time_cost = dataRecv['cost_time']

			       global route
			       route = [taxi["currentLoc"]]+dataRecv['route']

			else:
				retVal["message"] = "3.Your PWT is more"
				requestProcessed.append(retVal)
				continue

			print("cost for taxi",taxi['id'],":",cost," and taxis current loc:",taxi["currentLoc"]) 

			global direction

			startPoint = route[0]
			direction = []
			names_src = []
			names_dst = []

			pass_array = taxi["passenger"]+[{'src': [float(recieved['src_lat']),float(recieved['src_lon'])],'dest': [float(recieved['dest_lat']),float(recieved['dest_lon'])],"name":recieved["name"],"picked":0}]
			for i in route[1:]:
				path = giveRegionsPassed(startPoint,i)[:-1]
				res, name = check_src(i,names_src,pass_array)
				if(res):
				   path[len(path)-1]['src'] = 1
				   path[len(path)-1]['name'] = name
				   names_src.append(name)
				else:
				   res, name = check_dest(i,names_dst,names_src,pass_array)
				   if(res):
				     path[len(path)-1]['dest'] = 1
				     path[len(path)-1]['name'] = name
				     names_dst.append(name)
				direction += path
				startPoint = i

		    #return value to passenger
			retVal = {'name':  recieved["name"], 'id': taxi['id'], 'port':int(taxi_id), 'cost': cost,"detour_obj":detour_distance,"time_obj":dataRecv['cost_time']}

		    #check if passenger waiting time of all other current passengers changes a lot then broadcast request to other peers
			if(check_pwtime_constraint() == False):
				retVal["message"] = "4.PWT of other passenger"
				retVal["cost"] = -1
				requestProcessed.append(retVal)
				continue
		
			if(check_dsttime_constraint()==False):
				 retVal["message"] = "5. DRT of other passenger"
				 retVal["cost"] = -1
				 requestProcessed.append(retVal)
				 continue
		    
			if(taxi["noPassengers"]>0):
				 global t1
				 if(t1.is_alive):
				    t1.cancel()
			start_confirm_timer(recieved["name"])
			retVal["message"] = "6. success"
			requestProcessed.append(retVal)
			continue

	thread = threading.Thread(target=processRequest)
	thread.start()



def remove_nonexist_name(direction):
    index = 0
    for i in direction:
        if "name" in i:
            exist = False
            for j in taxi["passenger"]:
                if j["name"]==i["name"]:
                    exist = True
                    break
            if(exist==False):
                direction.pop(index)
        index += 1
    return direction

@app.route("/requestConfirm", methods = ['GET', 'POST'])
def confirmRequest():
    global taxi
    global direction
    global direction_dist
    global direction_time
    global taxi_detour_dist
    global request_in_process
    global request_in_process_timer
    global no_messages
    global shortest_path_aco
    global shortest_path_api
 
    recieved = request.args

    print("in request confirm...")
    taxi_detour_dist += float(recieved["current_detour"])   

    #when confirmation has come after 30 seconds, but it has already been reset by the timer and another request maybe in progress
    if(recieved["name"]!=request_in_process["passenger_name"]):
       if(taxi["noPassengers"]>0):
         reset_route_timer()
       return json.dumps({'delay_confirm':True})

    reset_confirm_timer() #cancel the timer since request is confirmed by passenger

    recieved = {'src': [float(recieved['src_lat']),float(recieved['src_lon'])],'dest': [float(recieved['dest_lat']),float(recieved['dest_lon'])],'name':recieved["name"]} 

    #fare = 78 + get_distance_api(recieved['src'],recieved['dest'])

    taxi['noPassengers'] += 1

    '''
    taxi['passenger'].append({'src': recieved['src'], 'dest': recieved['dest'],'name':recieved["name"],"picked":0, 'fare': fare,'passengerNo':taxi['noPassengers'],"elapsedTime":0})
    '''

    taxi['passenger'].append({'src': recieved['src'], 'dest': recieved['dest'],'name':recieved["name"],"picked":0,'passengerNo':taxi['noPassengers'],"elapsedTime":0})

    direction = remove_nonexist_name(direction)
    taxi["direction"] = direction

    #total distance and time to travel in this new direction
    taxi["total_dist"] = direction_dist
    taxi["total_time"] = direction_time
    
    #the way destination reaching time is computed is from the time the passenger is picked up -- needs change
    reach_time = find_destination_reachingtime(recieved["name"])
    taxi["passenger"][len(taxi["passenger"])-1]["DestReachTime"] = reach_time 

    ''' Remember this passenger waiting time is from current location at the time request arrived (startpoint = route[0]) to new passenger's source from API
	Should we consider current location - what if it changed by the time ACO and request confirmation happended??'''

    #add passenger waiting time
    passenger_waiting_time = find_pwaiting_time(recieved["name"])
    taxi["passenger"][taxi["noPassengers"]-1]["waitingTime"] = passenger_waiting_time

    shortest_path_api += get_distance_api(recieved['src'],recieved['dest']) #shortest-path distances between the pickup and drop-off locations of individual satisfied ride sharing requests using api 

    shortest_path_aco += get_distance_aco(recieved["name"])#shortest-path distances between the pickup and drop-off locations of individual satisfied ride sharing requests using aco
     
    if(taxi["noPassengers"]==1):
        start_route_timer()
    else:
        reset_route_timer()

    routeString = ""
    for i in route:
        routeString += str(i[0]) + "," + str(i[1]) + ";"
    routeString = routeString[:-1] 
    cost_params = {"route":routeString,"cost":cost, "name": recieved["name"]}

    
    r = requests.get(url=url_taxi+ params["seeder_port"] + "/getTaxisNearby",params={"src_lat":taxi['currentLoc'][0],"src_lon":taxi['currentLoc'][1]})
    data = r.json()


    print("About to broadcast to :",data)
    broadcast_taxi_ip = []
    if data['taxis'] == '[]':
       print("No taxi nearby to broadcast pheromone")
    else:
       taxi_ids = list(data['taxis'])
       broadcast_taxi_ip = [str(start_port + (int(temp_taxi_id)-1)) for temp_taxi_id in taxi_ids]
 
    #since its single threaded it will becomw a  loop if the same taxi is involved as a request
    broadcast_taxi_ip = list(set(broadcast_taxi_ip) - set([taxi_id])) 

    print("Broadcasting to :",broadcast_taxi_ip)
    if(len(broadcast_taxi_ip)>0):
       no_messages += 1 #broadcast messages
    threads_broadcast_pheromone = [threading.Thread(target=send_request_broadcast_pheromone, args=(i,cost_params)) for i in broadcast_taxi_ip]
    for thread in threads_broadcast_pheromone:
       thread.start()
    for thread in threads_broadcast_pheromone:
       thread.join()

    update_my_pheromone(cost_params)

    #plot_route()
    print("Done broadcasting..")
    #return json.dumps({'reach_time':reach_time,'fare':fare, 'pwt':passenger_waiting_time})

    #returning detour_cost and tot_time_cost (pareto)
    global detour_cost
    global tot_time_cost

    return json.dumps({'reach_time':reach_time, 'pwt':passenger_waiting_time,'passenger_no':taxi['noPassengers'],'taxi_id':taxi['id'],'detour_cost':detour_cost, 'tot_time_cost':tot_time_cost})



def update_my_pheromone(cost_params):
    global pheromone
    received = cost_params
    centroids_new = []
    route = received["route"]
    route = [list(map(float,i.split(','))) for i in route.split(";")]

    for i in route:
        pos = aco.convert_to_xy(i)
        pt = aco.get_nearest_centroid(pos)
        centroids_new.append(pt)
    for i in range(1,len(centroids_new)):
            try:
                pheromone[centroids_new[i-1]][centroids_new[i]] = (1-evaporation_factor)*pheromone[centroids_new[i-1]][centroids_new[i]] + evaporation_factor / float(received["cost"])
            except ZeroDivisionError:
                pheromone[centroids_new[i-1]][centroids_new[i]] = (1-evaporation_factor)*pheromone[centroids_new[i-1]][centroids_new[i]] + evaporation_factor / 999
    print("pheromone matrix updated for taxi id:",taxi["id"])
    return("Broadcasting Done.")

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
            try:
                pheromone[centroids_new[i-1]][centroids_new[i]] = (1-evaporation_factor)*pheromone[centroids_new[i-1]][centroids_new[i]] + evaporation_factor / float(received["cost"])
            except ZeroDivisionError:
                pheromone[centroids_new[i-1]][centroids_new[i]] = (1-evaporation_factor)*pheromone[centroids_new[i-1]][centroids_new[i]] + evaporation_factor / 999
    
    deleteRequest(received["name"], requestQueue)
    print("Deleted Request: ", received["name"])
    print("pheromone matrix updated for taxi id:",taxi["id"])
    return("Broadcasting Done.")

def find_rem_dist_with_2ormore_passengers():
	rem_dist = 0
	rem_time = 0

	no_pass = taxi["noPassengers"]
	for i in taxi["direction"]:
		if(no_pass >= 2):
			rem_dist += i["dist"]
			rem_time += i["time"]
		if "dest" in i:
			no_pass -= 1

	return (rem_dist,rem_time)
			

@app.route('/find_taxi_metric')
def find_taxi_metric():
	global taxi_total_dist
	global taxi_detour_dist
	global no_messages

	temp_dist = taxi_total_dist
	temp_time = 0
	for i in taxi["direction"]:
		temp_dist += i["dist"]
		temp_time += i["time"]
	
	return_value = find_rem_dist_with_2ormore_passengers()
	temp_dist_with_2ormore_passengers = return_value[0] + dist_with_2ormore_passengers
	rem_time = return_value[1]		
	return json.dumps({'total_distance_meters':temp_dist,'taxi_detour_dist':taxi_detour_dist,'no_messages':no_messages,"time_with_passenger":time_with_passenger,
"remain_time_in_direction":rem_time,"dist_with_2ormore_passengers":temp_dist_with_2ormore_passengers,"shortest_path_api":shortest_path_api,
"shortest_path_aco":shortest_path_aco,"rem_time_1pass":temp_time})


if __name__ == '__main__':

    app.run(host='127.0.0.1', port=int(taxi_id), debug = True,threaded=False)

