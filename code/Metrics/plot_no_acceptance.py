import pandas as pd
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

def no_acceptance(name,file_name_p):
	df = pd.read_csv(file_name_p)
	time = {2:0,3:0,4:0}
	time1 = {1:0,2:0,3:0}
	x = []
	for i,row in df.iterrows():
		if(row[3]>0):
			time[int(row[len(row)-1])] += 1
			x.append(i)


	#print(time)
	plt.bar(range(len(time)), list(time.values()), align='center')
	plt.xticks(range(len(time)), list(time1.keys()))
	plt.savefig(name + "_acceptance.png")
	plt.close()

	return time
