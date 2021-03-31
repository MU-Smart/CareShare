from queueModel import *
import csv
from pprint import pprint
requestQueue = []

passReqs = []


with open('./Pass_Requests/Sun_NonPeak_passenger.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	for row in csv_reader:
		passReqs.append(row)


for row in passReqs[:10]:
	src_lat = row[1]
	src_lon = row[2]
	dest_lat = row[3]
	dest_lon = row[4]
	name = row[0]
	request_params = {"src_lat":float(src_lat),"src_lon":float(src_lon),"dest_lat":float(dest_lat),"dest_lon":float(dest_lon),"name":name}
	requestQueue = acquireRequest(request_params, requestQueue)
	#print("Passenger Request Pushed")

print(len(requestQueue))
pprint(requestQueue)

print("###########################################################")
req = feed(requestQueue)
print(req) 
print(len(requestQueue))

print("##########################################################")

deleteRequest("4.0", requestQueue)
pprint(requestQueue)
