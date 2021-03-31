import pandas as pd
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

def calculate_mssg(m,file_name_t, file_name_p):
	df = pd.read_csv(file_name_t)
	mssg_taxi = []
	for i,row in df.iterrows():
		if(row[3]>0):	
			mssg_taxi.append(row[3])

	df = pd.read_csv(file_name_p)
	mssg_pass = []
	for i,row in df.iterrows():
		if(row[6]>0):	
			mssg_pass.append(row[6])

	#print(sum(mssg_taxi),sum(mssg_pass))
	#print("Ratio is :",(sum(mssg_taxi)+sum(mssg_pass))/2583)
	
	return (sum(mssg_taxi)+sum(mssg_pass))/m

