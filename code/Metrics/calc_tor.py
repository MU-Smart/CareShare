import pandas as pd
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt


def calculate_tor(t,file_name_t):
	df = pd.read_csv(file_name_t)
	time_with_pass = []
	rem_time = []
	num = []
	den = []

	for i,row in df.iterrows():
		if(row[4]>0 and row[5]>0):	
			num.append(row[4]+row[5])
			den.append(3600*t+row[9])

	#print(sum(num),sum(den))
	#print("Ratio is :",sum(num)/sum(den))
	
	return sum(num)/sum(den)

