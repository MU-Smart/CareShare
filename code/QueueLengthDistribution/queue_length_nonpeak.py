import json
import os
import matplotlib
import datetime
matplotlib.use("agg")
import matplotlib.pyplot as plt
import collections


fold = "./400_60T_90P/queue_log/"
non_peak_all = {}
non_peak_request = {}
non_peak_confirm = {}
non_peak_broadcast = {}



def init():
	global non_peak_all
	global non_peak_request
	global non_peak_confirm
	global non_peak_broadcast

	non_peak_all = {'18:00:00': 0, '19:45:00': 0, '20:00:00': 0, '14:20:00': 0, '16:25:00': 0, '18:35:00': 0, '15:05:00': 0, '15:10:00': 0, '16:10:00': 0, '17:05:00': 0, '20:25:00': 0, '18:15:00': 0, '14:55:00': 0, '18:25:00': 0, '14:30:00': 0, '18:50:00': 0, '18:30:00': 0, '19:05:00': 0, '20:05:00': 0, '19:30:00': 0, '15:45:00': 0, '18:05:00': 0, '16:30:00': 0, '15:55:00': 0, '19:00:00': 0, '17:35:00': 0, '19:50:00': 0, '17:10:00': 0, '15:00:00': 0, '18:40:00': 0, '17:30:00': 0, '16:50:00': 0, '17:15:00': 0, '19:40:00': 0, '18:20:00': 0, '16:35:00': 0, '19:35:00': 0, '16:05:00': 0, '17:25:00': 0, '15:40:00': 0, '16:40:00': 0, '19:55:00': 0, '17:00:00': 0, '16:00:00': 0, '17:40:00': 0, '15:25:00': 0, '14:35:00': 0, '19:20:00': 0, '20:20:00': 0, '15:50:00': 0, '18:55:00': 0, '18:10:00': 0, '16:45:00': 0, '14:25:00': 0, '15:35:00': 0, '16:55:00': 0, '20:15:00': 0, '15:15:00': 0, '14:50:00': 0, '14:40:00': 0, '17:45:00': 0, '17:55:00': 0, '16:15:00': 0, '15:20:00': 0, '15:30:00': 0, '14:45:00': 0, '17:50:00': 0, '19:10:00': 0, '16:20:00': 0, '19:15:00': 0, '14:15:00': 0, '18:45:00': 0, '17:20:00': 0, '20:10:00': 0, '19:25:00': 0,'14:10:00': 0}

	non_peak_request = {'18:00:00': 0, '19:45:00': 0, '20:00:00': 0, '14:20:00': 0, '16:25:00': 0, '18:35:00': 0, '15:05:00': 0, '15:10:00': 0, '16:10:00': 0, '17:05:00': 0, '20:25:00': 0, '18:15:00': 0, '14:55:00': 0, '18:25:00': 0, '14:30:00': 0, '18:50:00': 0, '18:30:00': 0, '19:05:00': 0, '20:05:00': 0, '19:30:00': 0, '15:45:00': 0, '18:05:00': 0, '16:30:00': 0, '15:55:00': 0, '19:00:00': 0, '17:35:00': 0, '19:50:00': 0, '17:10:00': 0, '15:00:00': 0, '18:40:00': 0, '17:30:00': 0, '16:50:00': 0, '17:15:00': 0, '19:40:00': 0, '18:20:00': 0, '16:35:00': 0, '19:35:00': 0, '16:05:00': 0, '17:25:00': 0, '15:40:00': 0, '16:40:00': 0, '19:55:00': 0, '17:00:00': 0, '16:00:00': 0, '17:40:00': 0, '15:25:00': 0, '14:35:00': 0, '19:20:00': 0, '20:20:00': 0, '15:50:00': 0, '18:55:00': 0, '18:10:00': 0, '16:45:00': 0, '14:25:00': 0, '15:35:00': 0, '16:55:00': 0, '20:15:00': 0, '15:15:00': 0, '14:50:00': 0, '14:40:00': 0, '17:45:00': 0, '17:55:00': 0, '16:15:00': 0, '15:20:00': 0, '15:30:00': 0, '14:45:00': 0, '17:50:00': 0, '19:10:00': 0, '16:20:00': 0, '19:15:00': 0, '14:15:00': 0, '18:45:00': 0, '17:20:00': 0, '20:10:00': 0, '19:25:00': 0,'14:10:00': 0}

	non_peak_confirm = {'18:00:00': 0, '19:45:00': 0, '20:00:00': 0, '14:20:00': 0, '16:25:00': 0, '18:35:00': 0, '15:05:00': 0, '15:10:00': 0, '16:10:00': 0, '17:05:00': 0, '20:25:00': 0, '18:15:00': 0, '14:55:00': 0, '18:25:00': 0, '14:30:00': 0, '18:50:00': 0, '18:30:00': 0, '19:05:00': 0, '20:05:00': 0, '19:30:00': 0, '15:45:00': 0, '18:05:00': 0, '16:30:00': 0, '15:55:00': 0, '19:00:00': 0, '17:35:00': 0, '19:50:00': 0, '17:10:00': 0, '15:00:00': 0, '18:40:00': 0, '17:30:00': 0, '16:50:00': 0, '17:15:00': 0, '19:40:00': 0, '18:20:00': 0, '16:35:00': 0, '19:35:00': 0, '16:05:00': 0, '17:25:00': 0, '15:40:00': 0, '16:40:00': 0, '19:55:00': 0, '17:00:00': 0, '16:00:00': 0, '17:40:00': 0, '15:25:00': 0, '14:35:00': 0, '19:20:00': 0, '20:20:00': 0, '15:50:00': 0, '18:55:00': 0, '18:10:00': 0, '16:45:00': 0, '14:25:00': 0, '15:35:00': 0, '16:55:00': 0, '20:15:00': 0, '15:15:00': 0, '14:50:00': 0, '14:40:00': 0, '17:45:00': 0, '17:55:00': 0, '16:15:00': 0, '15:20:00': 0, '15:30:00': 0, '14:45:00': 0, '17:50:00': 0, '19:10:00': 0, '16:20:00': 0, '19:15:00': 0, '14:15:00': 0, '18:45:00': 0, '17:20:00': 0, '20:10:00': 0, '19:25:00': 0,'14:10:00': 0}


	non_peak_broadcast ={'18:00:00': 0, '19:45:00': 0, '20:00:00': 0, '14:20:00': 0, '16:25:00': 0, '18:35:00': 0, '15:05:00': 0, '15:10:00': 0, '16:10:00': 0, '17:05:00': 0, '20:25:00': 0, '18:15:00': 0, '14:55:00': 0, '18:25:00': 0, '14:30:00': 0, '18:50:00': 0, '18:30:00': 0, '19:05:00': 0, '20:05:00': 0, '19:30:00': 0, '15:45:00': 0, '18:05:00': 0, '16:30:00': 0, '15:55:00': 0, '19:00:00': 0, '17:35:00': 0, '19:50:00': 0, '17:10:00': 0, '15:00:00': 0, '18:40:00': 0, '17:30:00': 0, '16:50:00': 0, '17:15:00': 0, '19:40:00': 0, '18:20:00': 0, '16:35:00': 0, '19:35:00': 0, '16:05:00': 0, '17:25:00': 0, '15:40:00': 0, '16:40:00': 0, '19:55:00': 0, '17:00:00': 0, '16:00:00': 0, '17:40:00': 0, '15:25:00': 0, '14:35:00': 0, '19:20:00': 0, '20:20:00': 0, '15:50:00': 0, '18:55:00': 0, '18:10:00': 0, '16:45:00': 0, '14:25:00': 0, '15:35:00': 0, '16:55:00': 0, '20:15:00': 0, '15:15:00': 0, '14:50:00': 0, '14:40:00': 0, '17:45:00': 0, '17:55:00': 0, '16:15:00': 0, '15:20:00': 0, '15:30:00': 0, '14:45:00': 0, '17:50:00': 0, '19:10:00': 0, '16:20:00': 0, '19:15:00': 0, '14:15:00': 0, '18:45:00': 0, '17:20:00': 0, '20:10:00': 0, '19:25:00': 0, '14:10:00': 0}

ct = 0
for fld in os.listdir(fold):
	all_req = []
	broadcast = []
	confirm = []
	request = []

	init()

	fld_name = "taxi_id_"+str(int(fld.split(".")[0])-400)
	with open(fold+fld) as f:
		d = json.load(f)

	for i in d["queue"]:
		all_req.append(datetime.datetime.strptime(i["timestamp"], "%H:%M:%S"))
		if(i["type"]=="getRequest"):
			request.append(datetime.datetime.strptime(i["timestamp"], "%H:%M:%S"))
		elif(i["type"]=="broadcastPheromone"):
			broadcast.append(datetime.datetime.strptime(i["timestamp"], "%H:%M:%S"))
		else:
			confirm.append(datetime.datetime.strptime(i["timestamp"], "%H:%M:%S"))
	all_req.sort()
	broadcast.sort()
	request.sort()
	confirm.sort()
	
	for i in all_req:
		done = 0
		for j in non_peak_all:
			t = datetime.datetime.strptime(j, "%H:%M:%S")
			if(i>=t and i <= t+datetime.timedelta(minutes=5)):
				non_peak_all[j] += 1
				done = 1
				break

		if(done!=1):
			print("error",i)


	for i in request:
		done = 0
		for j in non_peak_request:
			t = datetime.datetime.strptime(j, "%H:%M:%S")
			if(i>=t and i <= t+datetime.timedelta(minutes=5)):
				non_peak_request[j] += 1
				done = 1
				break

		if(done!=1):
			print("error",i)


	for i in confirm:
		done = 0
		for j in non_peak_confirm:
			t = datetime.datetime.strptime(j, "%H:%M:%S")
			if(i>=t and i <= t+datetime.timedelta(minutes=5)):
				non_peak_confirm[j] += 1
				done = 1
				break

		if(done!=1):
			print("error",i)

	for i in broadcast:
		done = 0
		for j in non_peak_broadcast:
			t = datetime.datetime.strptime(j, "%H:%M:%S")
			if(i>=t and i <= t+datetime.timedelta(minutes=5)):
				non_peak_broadcast[j] += 1
				done = 1
				break

		if(done!=1):
			print("error",i)

			
	'''print(non_peak_all)
	print(non_peak_broadcast)
	print(non_peak_request)
	print(non_peak_confirm)'''

	l = 0
	for i in non_peak_all:
		if(non_peak_all[i] != non_peak_request[i] + non_peak_confirm[i] + non_peak_broadcast[i]):
			print("========\nerror in count",i)
		l += non_peak_all[i]	

	print(l,len(all_req),l==len(all_req))

	non_peak_all = collections.OrderedDict(sorted(non_peak_all.items()))
	non_peak_broadcast = collections.OrderedDict(sorted(non_peak_broadcast.items()))
	non_peak_request = collections.OrderedDict(sorted(non_peak_request.items()))
	non_peak_confirm = collections.OrderedDict(sorted(non_peak_confirm.items()))
	
	os.mkdir("./Graphs_NonPeak/"+fld_name)	
	plt.bar([i*5 for i in range(0,len(non_peak_all))],non_peak_all.values())
	plt.xlabel("minute at which requests were received")
	plt.ylabel("request count")
	plt.savefig("./Graphs_NonPeak/"+fld_name+"/all_requests")
	plt.close()

	os.mkdir("./Graphs_NonPeak_All_requests/"+fld_name)	
	plt.bar([i*5 for i in range(0,len(non_peak_all))],non_peak_all.values())
	plt.xlabel("minute at which requests were received")
	plt.ylabel("request count")
	plt.savefig("./Graphs_NonPeak_All_requests/"+fld_name)
	plt.close()

	plt.bar([i*5 for i in range(0,len(non_peak_confirm))],non_peak_confirm.values())
	plt.xlabel("minute at which requests were received")
	plt.ylabel("request count")
	plt.savefig("./Graphs_NonPeak/"+fld_name+"/confirm")
	plt.close()

	plt.bar([i*5 for i in range(0,len(non_peak_request))],non_peak_request.values())
	plt.xlabel("minute at which requests were received")
	plt.ylabel("request count")
	plt.savefig("./Graphs_NonPeak/"+fld_name+"/request")
	plt.close()

	plt.bar([i*5 for i in range(0,len(non_peak_broadcast))],non_peak_broadcast.values())
	plt.xlabel("minute at which requests were received")
	plt.ylabel("request count")
	plt.savefig("./Graphs_NonPeak/"+fld_name+"/broadcast")
	plt.close()
	
	ct += 1
	if(ct==50):
		break
