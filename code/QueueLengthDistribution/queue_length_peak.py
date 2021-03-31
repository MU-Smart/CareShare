import json
import os
import matplotlib
import datetime
matplotlib.use("agg")
import matplotlib.pyplot as plt
import collections


fold = "./500_60T_90P/queue_log/"
peak_all = {}
peak_request = {}
peak_confirm = {}
peak_broadcast = {}



def init():
	global peak_all
	global peak_request
	global peak_confirm
	global peak_broadcast

	peak_all = {'16:00:00': 0, '16:20:00': 0, '14:40:00': 0, '14:50:00': 0, '15:10:00': 0, '14:30:00': 0, '16:45:00': 0, '17:30:00': 0, '16:25:00': 0, '17:10:00': 0, '16:55:00': 0, '15:45:00': 0, '15:40:00': 0, '17:40:00': 0, '16:50:00': 0, '17:05:00': 0, '14:20:00': 0, '15:50:00': 0, '15:15:00': 0, '14:45:00': 0, '17:20:00': 0, '15:05:00': 0, '16:35:00': 0, '17:15:00': 0, '16:05:00': 0, '17:35:00': 0, '16:30:00': 0, '14:25:00': 0, '14:55:00': 0, '17:00:00': 0, '14:35:00': 0, '15:55:00': 0, '15:00:00': 0, '14:15:00': 0, '16:40:00': 0, '16:10:00': 0, '17:25:00': 0, '15:20:00': 0, '15:25:00': 0, '15:35:00': 0, '15:30:00': 0, '16:15:00': 0,'14:10:00': 0}


	peak_request = {'16:00:00': 0, '16:20:00': 0, '14:40:00': 0, '14:50:00': 0, '15:10:00': 0, '14:30:00': 0, '16:45:00': 0, '17:30:00': 0, '16:25:00': 0, '17:10:00': 0, '16:55:00': 0, '15:45:00': 0, '15:40:00': 0, '17:40:00': 0, '16:50:00': 0, '17:05:00': 0, '14:20:00': 0, '15:50:00': 0, '15:15:00': 0, '14:45:00': 0, '17:20:00': 0, '15:05:00': 0, '16:35:00': 0, '17:15:00': 0, '16:05:00': 0, '17:35:00': 0, '16:30:00': 0, '14:25:00': 0, '14:55:00': 0, '17:00:00': 0, '14:35:00': 0, '15:55:00': 0, '15:00:00': 0, '14:15:00': 0, '16:40:00': 0, '16:10:00': 0, '17:25:00': 0, '15:20:00': 0, '15:25:00': 0, '15:35:00': 0, '15:30:00': 0, '16:15:00': 0,'14:10:00': 0}


	peak_confirm = {'16:00:00': 0, '16:20:00': 0, '14:40:00': 0, '14:50:00': 0, '15:10:00': 0, '14:30:00': 0, '16:45:00': 0, '17:30:00': 0, '16:25:00': 0, '17:10:00': 0, '16:55:00': 0, '15:45:00': 0, '15:40:00': 0, '17:40:00': 0, '16:50:00': 0, '17:05:00': 0, '14:20:00': 0, '15:50:00': 0, '15:15:00': 0, '14:45:00': 0, '17:20:00': 0, '15:05:00': 0, '16:35:00': 0, '17:15:00': 0, '16:05:00': 0, '17:35:00': 0, '16:30:00': 0, '14:25:00': 0, '14:55:00': 0, '17:00:00': 0, '14:35:00': 0, '15:55:00': 0, '15:00:00': 0, '14:15:00': 0, '16:40:00': 0, '16:10:00': 0, '17:25:00': 0, '15:20:00': 0, '15:25:00': 0, '15:35:00': 0, '15:30:00': 0, '16:15:00': 0,'14:10:00': 0}


	peak_broadcast = {'16:00:00': 0, '16:20:00': 0, '14:40:00': 0, '14:50:00': 0, '15:10:00': 0, '14:30:00': 0, '16:45:00': 0, '17:30:00': 0, '16:25:00': 0, '17:10:00': 0, '16:55:00': 0, '15:45:00': 0, '15:40:00': 0, '17:40:00': 0, '16:50:00': 0, '17:05:00': 0, '14:20:00': 0, '15:50:00': 0, '15:15:00': 0, '14:45:00': 0, '17:20:00': 0, '15:05:00': 0, '16:35:00': 0, '17:15:00': 0, '16:05:00': 0, '17:35:00': 0, '16:30:00': 0, '14:25:00': 0, '14:55:00': 0, '17:00:00': 0, '14:35:00': 0, '15:55:00': 0, '15:00:00': 0, '14:15:00': 0, '16:40:00': 0, '16:10:00': 0, '17:25:00': 0, '15:20:00': 0, '15:25:00': 0, '15:35:00': 0, '15:30:00': 0, '16:15:00': 0,'14:10:00': 0}

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
		for j in peak_all:
			t = datetime.datetime.strptime(j, "%H:%M:%S")
			if(i>=t and i <= t+datetime.timedelta(minutes=5)):
				peak_all[j] += 1
				done = 1
				break

		if(done!=1):
			print("error",i)


	for i in request:
		done = 0
		for j in peak_request:
			t = datetime.datetime.strptime(j, "%H:%M:%S")
			if(i>=t and i <= t+datetime.timedelta(minutes=5)):
				peak_request[j] += 1
				done = 1
				break

		if(done!=1):
			print("error",i)


	for i in confirm:
		done = 0
		for j in peak_confirm:
			t = datetime.datetime.strptime(j, "%H:%M:%S")
			if(i>=t and i <= t+datetime.timedelta(minutes=5)):
				peak_confirm[j] += 1
				done = 1
				break

		if(done!=1):
			print("error",i)

	for i in broadcast:
		done = 0
		for j in peak_broadcast:
			t = datetime.datetime.strptime(j, "%H:%M:%S")
			if(i>=t and i <= t+datetime.timedelta(minutes=5)):
				peak_broadcast[j] += 1
				done = 1
				break

		if(done!=1):
			print("error",i)

			
	'''print(peak_all)
	print(peak_broadcast)
	print(peak_request)
	print(peak_confirm)'''

	l = 0
	for i in peak_all:
		if(peak_all[i] != peak_request[i] + peak_confirm[i] + peak_broadcast[i]):
			print("========\nerror in count",i)
		l += peak_all[i]	

	print(l,len(all_req),l==len(all_req))

	peak_all = collections.OrderedDict(sorted(peak_all.items()))
	peak_broadcast = collections.OrderedDict(sorted(peak_broadcast.items()))
	peak_request = collections.OrderedDict(sorted(peak_request.items()))
	peak_confirm = collections.OrderedDict(sorted(peak_confirm.items()))
	
	os.mkdir("./Graphs_Peak/"+fld_name)	
	plt.bar([i*5 for i in range(0,len(peak_all))],peak_all.values())
	plt.xlabel("minute at which requests were received")
	plt.ylabel("request count")
	plt.savefig("./Graphs_Peak/"+fld_name+"/all_requests")
	plt.close()

	os.mkdir("./Graphs_Peak_All_requests/"+fld_name)	
	plt.bar([i*5 for i in range(0,len(peak_all))],peak_all.values())
	plt.xlabel("minute at which requests were received")
	plt.ylabel("request count")
	plt.savefig("./Graphs_Peak_All_requests/"+fld_name)
	plt.close()

	plt.bar([i*5 for i in range(0,len(peak_confirm))],peak_confirm.values())
	plt.xlabel("minute at which requests were received")
	plt.ylabel("request count")
	plt.savefig("./Graphs_Peak/"+fld_name+"/confirm")
	plt.close()

	plt.bar([i*5 for i in range(0,len(peak_request))],peak_request.values())
	plt.xlabel("minute at which requests were received")
	plt.ylabel("request count")
	plt.savefig("./Graphs_Peak/"+fld_name+"/request")
	plt.close()

	plt.bar([i*5 for i in range(0,len(peak_broadcast))],peak_broadcast.values())
	plt.xlabel("minute at which requests were received")
	plt.ylabel("request count")
	plt.savefig("./Graphs_Peak/"+fld_name+"/broadcast")
	plt.close()
	
	ct += 1
	if(ct==150):
		break
