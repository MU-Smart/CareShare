import pandas as pd


def find_dist(x,df_dataset):
	for i,row in df_dataset.iterrows():
		if(x==row[0]):
			return(row[len(row)-2]*1609.34)
	print(i)

def obtain_dist_ratio(pass_file,expt_file):
	df_expt = pd.read_csv(expt_file)

	df_dataset = pd.read_csv(pass_file)

	taxis = {}

	for i,row in df_expt.iterrows():
		if(row[0] > 0 and row[4] > 0):
			passenger_no = row[0]
			taxi = row[4]
			d = find_dist(int(passenger_no),df_dataset)
			if taxi in taxis:
				taxis[int(taxi)] += d
			else:
				taxis[int(taxi)] = d
	
	
	return taxis


#print(obtain_dist_ratio("Sun_NonPeak_passenger-duplicates.csv","experiments.csv"))
