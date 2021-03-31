import requests
import operator
import numpy as np

#url_taxi = "http://192.168.43.177:"
url_taxi = "http://0.0.0.0:"
print("Submitting request...")
all_taxi_ip = ["5000","5001","5002"]
taxi_ip = []
cost = []

passengerLoc = np.load("./Info/request.npy")

src = int(input("Enter Source: "))
dest = int(input("Enter Destination: "))
name = input("Name: ")

request_params = {"src_lat":passengerLoc[src-1][1],"src_lon":passengerLoc[src-1][0],"dest_lat":passengerLoc[dest-1][1],"dest_lon":passengerLoc[dest-1][0],"name":name}



for i in all_taxi_ip:
    r = requests.get(url=url_taxi+i+"/ping",params={"src_lat":request_params["src_lat"],"src_lon":request_params["src_lon"]})
    data = r.json()
    if(int(data["distance"]) < 3000):
        #print(data)
        taxi_ip.append(data["port"]) 

if(len(taxi_ip)==0):
	print("No taxi nearby to service you in first hop")
else:
	print("Forwarding request to taxis:",taxi_ip)

#taxi_ip = [5000]
for i in taxi_ip:
	r = requests.get(url=url_taxi+str(i)+"/getRequest",params=request_params)
	data = r.json()
	if(data["cost"]==-1):
		continue
	cost.append(data)


if(len(cost)>0):
	cost.sort(key=operator.itemgetter('cost'))
	#Send Confirmation Message
	print("taxi with id",cost[0]["id"]," confirmed")
	r = requests.get(url=url_taxi+str(cost[0]["port"])+"/requestConfirm",params=request_params)
	data = r.json()
	print("Dest reach time:",data["reach_time"],"seconds and your expected fare is:",data['fare'])
else:
	print("Sorry no taxi can service you")
