import requests
import operator
import numpy as np
import sys
import csv
import time
import datetime
import threading
import json
import random
from rideShare_parameters import get_parameters

params = get_parameters()

url_taxi = params["url_taxi_ip"]
print("Submitting request...")
no_of_taxis = int(params["no_of_taxis"])
start_port = int(params["start_port"])

all_taxi_ip = [str(start_port+i) for i in range(no_of_taxis)]
taxi_ip = []
cost = []
row = []
res_op = {}
#passengerLoc = np.load("./Info/request.npy")
no_messages = 0

src_lat = sys.argv[1]
src_lon = sys.argv[2]
dest_lat = sys.argv[3]
dest_lon = sys.argv[4]
name = sys.argv[5]


request_params = {"src_lat":float(src_lat),"src_lon":float(src_lon),"dest_lat":float(dest_lat),"dest_lon":float(dest_lon),"name":name}

def send_request(port,broadcast_taxis,messg):
	global cost
	try:
		params=request_params
		params["taxi"]=port
		params["all_broadcasted_taxis"] = broadcast_taxis
		params["timestamp"] = datetime.datetime.now().strftime("%H:%M:%S")
		r = requests.get(url=url_taxi+str(port)+"/getRequest",params=params, timeout=60)
		data = r.json()
		if(data["cost"]!=-1):
			cost.append(data)
		else:
			if("message" in data):
				messg.append(data["message"])
			else:
				data["other_message"]= "other..."
				messg.append(data)
	except Exception as e:
		messg.append("Connection timed out") 
		print(e)


def find_paretoSoln(soln):
	pareto = []
	for i in range(0,len(soln)):
		non_dominated = 0
		for j in range(0,len(soln)):
			if(i!=j):
				#check for dominance
				if((soln[j]["detour_obj"] <= soln[i]["detour_obj"] and soln[j]["time_obj"] <= soln[i]["time_obj"]) and (soln[j]["detour_obj"] < soln[i]["detour_obj"] or soln[j]["time_obj"] < soln[i]["time_obj"])):
					break
				else:#when it is non dominated
					non_dominated += 1
		if(non_dominated == len(soln)-1):
			pareto.append(soln[i])
	return pareto


def request(reqno):
	if reqno>1:
		rand_sleep = random.randint(1,300)
		time.sleep(rand_sleep)

	start_time = datetime.datetime.now()
	r = requests.get(url=url_taxi + params["seeder_port"] + "/getTaxisNearby",params={"src_lat":request_params["src_lat"],"src_lon":request_params["src_lon"],"name":name})
	data = r.json()

	global cost
	global row
	global no_messages
	global res_op

	cost = []
	taxi_ip = []
	taxi_ids = list(data['taxis'])
	taxi_ip = [str(start_port + (int(taxi_id)-1)) for taxi_id in taxi_ids] 
	res_op = {}
	messg = []

	if(len(taxi_ip)==0):
		messg = ["No taxi in first hop"]
		res_op["message"] = messg
		print("No taxi nearby to service you in first hop")
		end_time = datetime.datetime.now()
		#added two more value detour_cost, tot_time_cost (pareto)
		row = [name, 'NA', 'NA','NA','NA',(end_time -start_time).total_seconds(),no_messages,0,reqno, 'NA', 'NA']
		return False
	else:
		print("Forwarding request to taxis:",taxi_ip)
		broadcast_taxis = " ".join(str(x) for x in taxi_ip)
		no_messages += 1#broadcast message
		threads = [threading.Thread(target=send_request, args=(i,broadcast_taxis,messg)) for i in taxi_ip]
		for thread in threads:
		    thread.start()
		for thread in threads:
		    thread.join()
		no_messages += len(taxi_ip) #reply from taxi messages
		print("request sent ....")
		#name, pwt,dst,passenger_no,taxi_id which served it ,time to process request, no_messages,no_taxis, detour_cost, tot_time_cost (pareto)
		row = [name, 'NA', 'NA', 'NA','NA','NA',no_messages,0,reqno, 'NA', 'NA']

		if(len(cost)>0):
			pareto = find_paretoSoln(cost)
			if(len(pareto)==0):
				cost.sort(key=operator.itemgetter('cost'))
				detour_obj = 'NA'
				time_obj = 'NA'
			else:
				pareto_optimal = random.choice(pareto)
				cost = [pareto_optimal]
				print(cost)
				detour_obj = cost[0]["detour_obj"]
				time_obj = cost[0]["time_obj"]
			#Send Confirmation Message
			request_params["taxi_id"] = cost[0]["id"]
			request_params["current_detour"] = cost[0]["cost"]
			request_params["name"] = name
			print("Sending confirmation....")
			no_messages += 1 #sending confirm
			r = requests.get(url=url_taxi+str(cost[0]["port"])+"/requestConfirm",params=request_params)
			print(r)
			data = r.json()
			end_time = datetime.datetime.now()
			if "delay_confirm" in data:
				print("Sorry there was a delay, no taxi to service")
				res_op["message"] = "Delay in Confirmation"
				#added two more value detour_cost, tot_time_cost (pareto)
				row = [name, 'NA', 'NA','NA','NA',(end_time -start_time).total_seconds(),no_messages,len(taxi_ip),reqno,'NA','NA']
				return False
			else:
				no_messages += 1 #taxi side confirm
				print("taxi with id",cost[0]["id"]," confirmed")
				print("Dest reach time:",data["reach_time"],"seconds")
				#added two more value detour_cost, tot_time_cost (pareto)
				print(cost,"Detour: ",detour_obj,"\nTotal travel time:", time_obj)		
				row = [name, data['pwt'], data["reach_time"],data['passenger_no'],data['taxi_id'],(end_time -start_time).total_seconds(),no_messages,len(taxi_ip),reqno,detour_obj ,time_obj]
				return True
		else:
			end_time = datetime.datetime.now()
			#added two more value detour_cost, tot_time_cost (pareto)
			row = [name, 'NA', 'NA','NA','NA',(end_time -start_time).total_seconds(),no_messages,len(taxi_ip),reqno, 'NA', 'NA']
			res_op["message"] = messg
			print("Sorry no taxi can service you")
			return False

no_of_req_sent = 1
rand_iterations = random.randint(2,4)
for i in range(1,rand_iterations):
	no_of_req_sent += 1
	status_success = request(i)
	if(status_success):
		break

if(status_success!=True):
	no_of_req_sent = 'NA'
	with open('./json_log/'+name+'.json', 'w') as outfile:
		json.dump(res_op, outfile)

row.append(no_of_req_sent)
with open("experiments.csv","a") as results_file:
	csv_writer = csv.writer(results_file)
	csv_writer.writerow(row)
results_file.close()
