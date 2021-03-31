import pandas as pd
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
import dist_ratio_dataset

def calculate_distance_ratio(file_name_t,pass_file,expt_file):
	taxis = dist_ratio_dataset.obtain_dist_ratio(pass_file,expt_file)
	df = pd.read_csv(file_name_t)
	aco = []
	dataset = []
	x = []
	for i,row in df.iterrows():
		num_dataset = 0
		den = 0
		num_aco = 0
		if(i==0):
			mul = int(row[0]) 
		if(row[0] >= 0):
			if int(row[0])-mul+1 in taxis:
				num_dataset=taxis[int(row[0])-mul+1]
		if(row[6]>0):
			den=row[6]	
		if(row[8]>0):
			num_aco=row[8]
		if(den>0 and num_dataset>0 and num_aco>0):
			aco.append(num_aco/den)
			dataset.append(num_dataset/den)
	#print(len(den),len(num_aco),len(num_api))
	#print("ACO:",sum(num_aco),sum(den), sum(num_aco)/sum(den))	
	#print("API:", sum(num_api),sum(den),sum(num_api)/sum(den))	

	return sum(aco)/len(aco),sum(dataset)/len(dataset)
