import requests
import operator
import numpy as np
import csv
from rideShare_parameters import get_parameters

params = get_parameters()

no_of_taxis = int(params["no_of_taxis"])
url_taxi = params["url_taxi_ip"]
start_port = int(params["start_port"])


all_taxi_ip = [str(start_port+i) for i in range(no_of_taxis)]

with open(params["results_csv_file"],"a") as results_file:
		csv_writer = csv.writer(results_file)
		csv_writer.writerow(["id","total_dist","total_detour","no_messages","time_with_passenger","remain_time_in_direction",
"dist_with_2ormore_passengers","shortest_path_api","shortest_path_aco","rem_time_1pass"])

for i in all_taxi_ip:
	r = requests.get(url=url_taxi+i+"/find_taxi_metric")
	data = r.json()
	row = [i,data['total_distance_meters'],data['taxi_detour_dist'],data['no_messages'],data['time_with_passenger'],data["remain_time_in_direction"],data["dist_with_2ormore_passengers"],data["shortest_path_api"],data["shortest_path_aco"],data["rem_time_1pass"]]
	with open("experiments_taxis.csv","a") as results_file:
		csv_writer = csv.writer(results_file)
		csv_writer.writerow(row)
results_file.close()
