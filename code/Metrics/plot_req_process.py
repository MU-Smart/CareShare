import pandas as pd
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt


def req_process(file_name_p):
	df = pd.read_csv(file_name_p)
	time = []
	x = []
	for i,row in df.iterrows():
		if(row[5]>0):
			time.append(row[5])
			x.append(i)

	#print(sum(time)/len(time))
	'''plt.plot(x,time)
	plt.xlabel("requests")
	plt.ylabel("req process time(sec)")
	plt.savefig("time_reqprocess.png")'''
	return sum(time)/len(time)
