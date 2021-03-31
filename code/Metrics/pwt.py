import pandas as pd
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

def wait_time(file_name_p):
	df = pd.read_csv(file_name_p)
	time = []
	x = []
	for i,row in df.iterrows():
		if(row[1]>0):
			time.append(row[1])
			x.append(i)

	return sum(time)/len(time)
