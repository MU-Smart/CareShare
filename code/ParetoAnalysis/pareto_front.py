import json
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import os

fld_ct = 0
for i in os.listdir("./PassReq_ParetoFront/NonPeak/Pareto/"):
	print(i)
	if(fld_ct==100):
		break
	fld_ct += 1
	with open("./PassReq_ParetoFront/NonPeak/Pareto/"+i) as f:
		data = json.load(f)

	try:
		d = []
		t = []
		
		for j in data["all"]:
			all_soln = plt.scatter(j["detour_obj"],j["time_obj"],color='blue')
			d.append(j["detour_obj"])
			t.append(j["time_obj"])
			

		for j in data["pareto_front"]:
			non_dom = plt.scatter(j["detour_obj"],j["time_obj"],color='red')
			d.append(j["detour_obj"])
			t.append(j["time_obj"])

		if "multiple_pareto" in data:
			knee_point = plt.scatter(data["multiple_pareto"]["detour_obj"],data["multiple_pareto"]["time_obj"],color="green")

		'''if "no_pareto" in data:
			plt.scatter(data["no_pareto"]["detour_obj"],data["no_pareto"]["time_obj"],color="green")'''

		if(min(d) <0):
			print("D:",min(d))

		if(min(t) <0):
			print("T:",min(t))		

		plt.xlabel("Detour in meter")
		plt.ylabel("Time in seconds")
		plt.xlim(0,max(d)+100)
		plt.ylim(0,max(t)+100)
		plt.legend((all_soln,non_dom,knee_point),('All solution', 'Pareto front', 'Knee point'),loc='upper left',fontsize=8)
		
		plt.savefig("./Graphs_KneePoint_MinDist/NonPeak/"+i.split(".")[0])
		
		plt.close()

	except:
		continue
