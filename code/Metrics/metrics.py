import success_rate
import plot_cap_reqno
import calc_tor
import calc_mssg
import calc_dist_ratio
import plot_no_acceptance
import pwt
import plot_req_process
import os
import json
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

final_p = {"success":0,"dist_ratio_aco":0,"req_process":0,"pwt":0,"mssg":0,"tor":0,"dist_ratio_dataset":0}
final_cap_p = {1:0,2:0,3:0,4:0}
final_acceptance_p = {2:0,3:0,4:0}


final_np = {"success":0,"dist_ratio_aco":0,"req_process":0,"pwt":0,"mssg":0,"tor":0,"dist_ratio_dataset":0}
final_cap_np = {1:0,2:0,3:0,4:0}
final_acceptance_np = {2:0,3:0,4:0}

no_iterations = 1
time1 = {1:0,2:0,3:0}

for iteration in os.listdir("./Iterations"):
	for fold in os.listdir("./Iterations/"+iteration):
		if "400" in fold:
			#non peak
			segment_day = 6
			dist_dataset_file = "./Sun_NonPeak_passenger-duplicates.csv"
			
		elif "500" in fold:
			#peak
			segment_day = 3
			dist_dataset_file = "./Sun_Peak_passenger-duplicates.csv"

		file_name_p = "./Iterations/"+iteration + "/" + fold +"/experiments.csv"
		file_name_t = "./Iterations/"+iteration + "/" + fold +"/experiments_taxis.csv"

		print(file_name_p,file_name_t)
		success, s_rate = success_rate.get_success_rate(file_name_p)

		dist_ratio_aco,dist_ratio_dataset = calc_dist_ratio.calculate_distance_ratio(file_name_t,dist_dataset_file,file_name_p)

		tor = calc_tor.calculate_tor(segment_day,file_name_t)

		mssg = calc_mssg.calculate_mssg(success,file_name_t, file_name_p)

		req_process_time = plot_req_process.req_process(file_name_p)

		cap = plot_cap_reqno.cap_reqno("./Cap/"+iteration+"_"+fold,file_name_p)

		accept = plot_no_acceptance.no_acceptance("./Acceptance/"+iteration+"_"+fold,file_name_p)

		pass_wait = pwt.wait_time(file_name_p)


		d = {"success_rate":s_rate,"distance_ratio_aco":dist_ratio_aco,"tor":tor,"mssg":mssg,"req_process":req_process_time,"pwt":pass_wait,"distance_ratio_dataset":dist_ratio_dataset}

		if "500" in fold:
			final_p["success"] += s_rate
			final_p["dist_ratio_aco"] += dist_ratio_aco
			final_p["dist_ratio_dataset"] += dist_ratio_dataset
			final_p["pwt"] += pass_wait
			final_p["tor"] += tor
			final_p["mssg"] += mssg
			final_p["req_process"]+= req_process_time

			for k in cap:
				final_cap_p[k] += cap[k]
			for k in accept:
				final_acceptance_p[k] += accept[k]

		if "400" in fold:
			final_np["success"] += s_rate
			final_np["dist_ratio_aco"] += dist_ratio_aco
			final_np["dist_ratio_dataset"] += dist_ratio_dataset
			final_np["pwt"] += pass_wait
			final_np["tor"] += tor
			final_np["mssg"] += mssg
			final_np["req_process"]+= req_process_time

			for k in cap:
				final_cap_np[k] += cap[k]
			for k in accept:
				final_acceptance_np[k] += accept[k]		
		#print("Final is:", d)
		with open ("./JSON/"+iteration+"_"+fold+".json", 'w')as fp:
			json.dump(d, fp)


for i in final_p:
	final_p[i] = final_p[i] /no_iterations

for i in final_cap_p:
	final_cap_p[i] = final_cap_p[i] /no_iterations

for i in final_acceptance_p:
	final_acceptance_p[i] = final_acceptance_p[i] /no_iterations


print("Final peak cap is:",final_cap_p)
print("Final peak acceptance is:",final_acceptance_p)
print("Final Peak is:",final_p)

plt.bar(range(len(final_cap_p)), list(final_cap_p.values()), align='center')
plt.xticks(range(len(final_cap_p)), list(final_cap_p.keys()))
plt.ylabel("success rate of passenger req")
plt.xlabel("capacity")
plt.savefig("cap_p.png")
plt.close()

plt.bar(range(len(final_acceptance_p)), list(final_acceptance_p.values()), align='center')
plt.xticks(range(len(final_acceptance_p)), list(time1.keys()))
plt.savefig("acceptance_p.png")
plt.close()

for i in final_np:
	final_np[i] = final_np[i] /no_iterations

for i in final_cap_np:
	final_cap_np[i] = final_cap_np[i] /no_iterations

for i in final_acceptance_np:
	final_acceptance_np[i] = final_acceptance_np[i] /no_iterations


print("Final nonpeak cap is:",final_cap_np)
print("Final nonpeak acceptance is:",final_acceptance_np)
print("Final NonPeak is:",final_np)

plt.bar(range(len(final_cap_np)), list(final_cap_np.values()), align='center')
plt.xticks(range(len(final_cap_np)), list(final_cap_np.keys()))
plt.ylabel("success rate of passenger req")
plt.xlabel("capacity")
plt.savefig("cap_np.png")
plt.close()

plt.bar(range(len(final_acceptance_np)), list(final_acceptance_np.values()), align='center')
plt.xticks(range(len(final_acceptance_np)), list(time1.keys()))
plt.savefig("acceptance_np.png")
plt.close()

