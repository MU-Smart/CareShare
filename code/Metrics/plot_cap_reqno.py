import pandas as pd
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt


def cap_reqno(name,file_name_p):
	df = pd.read_csv(file_name_p)
	time = {1:0,2:0,3:0,4:0}
	x = []
	for i,row in df.iterrows():
		if(row[3]>0):
			time[int(row[3])] += 1
			x.append(i)

	print(time)
	s = 0
	for i in time:
		s += time[i]
	for i in time:
		time[i] = time[i]/s
	print(time)
	plt.bar(range(len(time)), list(time.values()), align='center')
	plt.xticks(range(len(time)), list(time.keys()))
	plt.ylabel("success rate of passenger req")
	plt.xlabel("capacity")
	plt.savefig(name+ "_cap.png")

	plt.close()

	return time
