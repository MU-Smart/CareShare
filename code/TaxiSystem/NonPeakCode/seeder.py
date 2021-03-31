import csv
import numpy as np
import AntColonyAlgo.ACO as aco
from flask import Flask
from flask import request
import json
import math
import requests
from threading import Timer
from rideShare_parameters import get_parameters

app = Flask(__name__)

taxis_in_grids = {}
taxi_locations = []

params = get_parameters()

centroids = np.load(params["centroids_file"])
n_grids = centroids.shape[0]

no_of_taxis = int(params["no_of_taxis"])
start_port = int(params["start_port"])
url_taxi = params["url_taxi_ip"]

with open(params["taxi_init_file"]) as taxi:
	csv_reader = csv.reader(taxi,delimiter=',')
	taxi_id = 1
	for row in csv_reader:
		taxi_locations.append([float(row[0]),float(row[1])])
		grid_no = aco.get_nearest_centroid(aco.convert_to_xy([float(row[0]),float(row[1])]))
		if grid_no in taxis_in_grids:
			taxis_in_grids[grid_no].append(taxi_id)
		else:
			taxis_in_grids[grid_no] = [taxi_id]
		taxi_id += 1

def remove_previous_grid_loc(taxi_no):
	for i in taxis_in_grids:
		if(taxi_no in taxis_in_grids[i]):
			taxis_in_grids[i].remove(taxi_no)
			break

def update_taxi_location():
	global taxi_locations
	global t
	print("updating...")
	temp_taxi_locations = []
	for i in range(start_port,start_port+taxi_id-1):
		r = requests.get(url=url_taxi+str(i)+"/liveTrack")
		data = r.json()
		taxiLoc = data['curr']
		grid_no = aco.get_nearest_centroid(aco.convert_to_xy([float(taxiLoc[0]),float(taxiLoc[1])]))
		temp_taxi_locations.append([float(taxiLoc[0]),float(taxiLoc[1])])
		remove_previous_grid_loc(int(i)-start_port+1)
		if grid_no in taxis_in_grids:
			taxis_in_grids[grid_no].append(int(i)-start_port+1)
		else:
			taxis_in_grids[grid_no] = [int(i)-start_port+1]
	taxi_locations = temp_taxi_locations
	if(t.is_alive):
		t.cancel()
		t = Timer(int(params['update_taxi_location_timer']),update_taxi_location)
		t.start()

t = Timer(int(params['update_taxi_location_timer']), update_taxi_location)
t.start() 

@app.route("/getTaxis", methods = ['GET', 'POST'])
def get_nearest_taxis():
	recieved = request.args
	passLoc = [float(recieved['src_lat']),float(recieved['src_lon'])]
	grid_no = aco.get_nearest_centroid(aco.convert_to_xy(passLoc))
	if grid_no in taxis_in_grids:
		return(json.dumps({'taxis': taxis_in_grids[grid_no]}))
	else:
		return(json.dumps({'taxis': []}))

@app.route("/getTaxisNearby", methods = ['GET', 'POST'])
def get_next_hop():
	recieved = request.args
	passLoc = [float(recieved['src_lat']),float(recieved['src_lon'])]
	x1,y1 = aco.convert_to_xy(passLoc)
	taxi_ids = []
	for (t_id, taxi_loc) in enumerate(taxi_locations):
		x2,y2 = aco.convert_to_xy(taxi_loc)   
		dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
		if dist < 500:
			taxi_ids.append(t_id+1)
	return(json.dumps({'taxis': taxi_ids}))

if __name__ == "__main__":
	app.run(host='127.0.0.1', port=int(params["seeder_port"]), debug = True,threaded=False)
